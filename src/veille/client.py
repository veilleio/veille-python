"""Blocking and async-I/O Veille clients backed by HTTPX."""

from __future__ import annotations

import asyncio
import os
import time
from collections.abc import Awaitable, Callable, Iterable, Mapping
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Literal, Self, TypeVar
from urllib.parse import urlsplit

import httpx

from ._endpoints import ENDPOINTS
from ._operations import _AsyncOperations, _SyncOperations
from ._response import create_api_error, create_raw_response, decode_success_response
from ._serialization import encode_json_body, encode_query, serialize_request
from ._version import __version__
from .errors import (
    VeilleConfigurationError,
    VeilleJobTimeoutError,
    VeilleSerializationError,
    VeilleTransportError,
)
from .models import APIResponse, BatchResult, HTTPMethod, JsonResponse, RawResponse, RequestOptions

_I = TypeVar("_I")
_T = TypeVar("_T")

DEFAULT_BASE_URL = "https://api.veille.io"
DEFAULT_TIMEOUT = 120.0
DEFAULT_CONCURRENCY = 10
"""Tasks run at the same time by ``batch()``."""
MAX_RETRIES = 3
"""Retries after a network error or a 408, 429, 500, 502, 503 or 504 response."""
RETRY_BACKOFF_FACTOR = 1.5
"""Each retry waits this many times longer than the previous one (a Retry-After header wins)."""
DEFAULT_RETRY_DELAY = 1.0
"""Seconds before the first retry."""
MAX_RETRY_DELAY = 30.0
RETRYABLE_STATUSES = frozenset({408, 500, 502, 503, 504})
API_KEY_ENVIRONMENT_VARIABLE = "VEILLE_API_KEY"
JOB_TERMINAL_STATUSES = frozenset({"CompletedJob", "Error", "NotFound", "BadRequest"})
MAX_POLL_INTERVAL = 60.0


@dataclass(frozen=True, slots=True)
class _Configuration:
    api_key: str
    base_url: str
    timeout: float | None
    headers: Mapping[str, str]
    max_retries: int
    retry_delay: float


@dataclass(frozen=True, slots=True)
class _PreparedRequest:
    method: HTTPMethod
    url: str
    headers: dict[str, str]
    content: bytes | None
    timeout: float | None
    expected: Literal["json", "any"]
    max_retries: int


class VeilleClient(_SyncOperations):
    """Reusable blocking Veille client. Use it as a context manager or call ``close()``."""

    __slots__ = ("_closed", "_configuration", "_http_client", "_owns_http_client")

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | None = DEFAULT_TIMEOUT,
        headers: Mapping[str, str] | None = None,
        max_retries: int = MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        http_client: httpx.Client | None = None,
    ) -> None:
        self._configuration = _build_configuration(
            api_key, base_url, timeout, headers, max_retries, retry_delay
        )
        if http_client is not None and not isinstance(http_client, httpx.Client):
            raise VeilleConfigurationError("http_client must be an httpx.Client when provided.")
        self._owns_http_client = http_client is None
        self._http_client = http_client or httpx.Client(follow_redirects=False)
        self._closed = False

    def request(
        self,
        method: HTTPMethod,
        path: str,
        params: Mapping[str, Any] | None = None,
        *,
        timeout: float | None = None,
        headers: Mapping[str, str] | None = None,
        max_retries: int | None = None,
    ) -> APIResponse:
        """Send any request to the Veille API, including endpoints newer than this SDK."""

        options = RequestOptions(
            method=method, timeout=timeout, headers=headers, max_retries=max_retries
        )
        return self._send(_prepare(self._configuration, method, path, params, options, "any"))

    def batch(
        self,
        items: Iterable[_I],
        task: Callable[[_I], _T],
        *,
        concurrency: int = DEFAULT_CONCURRENCY,
    ) -> list[BatchResult[_T]]:
        """Run ``task`` for every item on ``concurrency`` threads (default 10).

        Returns one :class:`BatchResult` per item, in input order; a failing item never stops the others.
        The client is thread-safe, so ``task`` can call its methods directly.
        """

        _check_concurrency(concurrency)
        values = list(items)
        if not values:
            return []
        with ThreadPoolExecutor(max_workers=min(concurrency, len(values))) as pool:
            futures = [pool.submit(task, value) for value in values]
        return [_settle(index, future) for index, future in enumerate(futures)]

    def wait_for_job(
        self,
        job_id: str,
        *,
        interval: float = 3.0,
        timeout: float = 43_200.0,
        on_progress: Callable[[Any], None] | None = None,
    ) -> JsonResponse:
        """Poll ``GET /v1/jobs/{id}`` until the job reaches a terminal status.

        Polls after ``interval`` seconds, then 1.5x longer each time up to 60 s. Raises
        ``VeilleJobTimeoutError`` after ``timeout`` seconds (default 12 hours).
        """

        _check_job_id(job_id)
        started = time.monotonic()
        while True:
            last = self.request("GET", "/v1/jobs/{id}", {"id": job_id})
            if not isinstance(last, JsonResponse):
                raise VeilleTransportError("The job endpoint did not return JSON.", TypeError())
            if on_progress is not None:
                on_progress(last.data)
            if _is_terminal(last.data):
                return last
            if time.monotonic() - started + interval > timeout:
                raise VeilleJobTimeoutError(job_id, last)
            time.sleep(interval)
            interval = _next_interval(interval)

    def close(self) -> None:
        """Close transport resources owned by this client."""

        if self._closed:
            return
        try:
            if self._owns_http_client:
                self._http_client.close()
        finally:
            self._closed = True

    def __enter__(self) -> Self:
        self._ensure_open()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def _call(
        self, name: str, params: dict[str, Any], options: RequestOptions | None
    ) -> APIResponse:
        return self._send(_prepare_operation(self._configuration, name, params, options))

    def _send(self, prepared: _PreparedRequest) -> APIResponse:
        self._ensure_open()
        attempt = 0
        while True:
            try:
                response = self._http_client.request(
                    prepared.method,
                    prepared.url,
                    headers=prepared.headers,
                    content=prepared.content,
                    timeout=prepared.timeout,
                    follow_redirects=False,
                )
                body = response.read()
            except httpx.TimeoutException as cause:
                raise VeilleTransportError("Veille request timed out.", cause) from cause
            except Exception as cause:
                if attempt < prepared.max_retries:
                    time.sleep(_retry_delay(self._configuration.retry_delay, attempt, None))
                    attempt += 1
                    continue
                raise VeilleTransportError(
                    "Veille request failed before an HTTP response body was received.", cause
                ) from cause
            raw_response = create_raw_response(response, body)
            if _is_retryable(raw_response) and attempt < prepared.max_retries:
                retry_after = (raw_response.headers.get("retry-after") or (None,))[0]
                time.sleep(_retry_delay(self._configuration.retry_delay, attempt, retry_after))
                attempt += 1
                continue
            return _decode(raw_response, prepared)

    def _ensure_open(self) -> None:
        if self._closed:
            raise VeilleConfigurationError("This VeilleClient is closed.")


class AsyncVeilleClient(_AsyncOperations):
    """Reusable async-I/O Veille client. Use it as an async context manager or await ``aclose()``."""

    __slots__ = ("_closed", "_configuration", "_http_client", "_owns_http_client")

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str | None = None,
        timeout: float | None = DEFAULT_TIMEOUT,
        headers: Mapping[str, str] | None = None,
        max_retries: int = MAX_RETRIES,
        retry_delay: float = DEFAULT_RETRY_DELAY,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        self._configuration = _build_configuration(
            api_key, base_url, timeout, headers, max_retries, retry_delay
        )
        if http_client is not None and not isinstance(http_client, httpx.AsyncClient):
            raise VeilleConfigurationError(
                "http_client must be an httpx.AsyncClient when provided."
            )
        self._owns_http_client = http_client is None
        self._http_client = http_client or httpx.AsyncClient(follow_redirects=False)
        self._closed = False

    async def request(
        self,
        method: HTTPMethod,
        path: str,
        params: Mapping[str, Any] | None = None,
        *,
        timeout: float | None = None,
        headers: Mapping[str, str] | None = None,
        max_retries: int | None = None,
    ) -> APIResponse:
        """Send any request to the Veille API, including endpoints newer than this SDK."""

        options = RequestOptions(
            method=method, timeout=timeout, headers=headers, max_retries=max_retries
        )
        return await self._send(_prepare(self._configuration, method, path, params, options, "any"))

    async def batch(
        self,
        items: Iterable[_I],
        task: Callable[[_I], Awaitable[_T]],
        *,
        concurrency: int = DEFAULT_CONCURRENCY,
    ) -> list[BatchResult[_T]]:
        """Await ``task`` for every item with at most ``concurrency`` in flight (default 10).

        Returns one :class:`BatchResult` per item, in input order; a failing item never stops the others.
        """

        _check_concurrency(concurrency)
        semaphore = asyncio.Semaphore(concurrency)

        async def run(index: int, value: _I) -> BatchResult[_T]:
            async with semaphore:
                try:
                    return BatchResult(index=index, value=await task(value))
                except Exception as error:
                    return BatchResult(index=index, error=error)

        return list(await asyncio.gather(*(run(i, v) for i, v in enumerate(items))))

    async def wait_for_job(
        self,
        job_id: str,
        *,
        interval: float = 3.0,
        timeout: float = 43_200.0,
        on_progress: Callable[[Any], None] | None = None,
    ) -> JsonResponse:
        """Poll ``GET /v1/jobs/{id}`` until the job reaches a terminal status."""

        _check_job_id(job_id)
        started = time.monotonic()
        while True:
            last = await self.request("GET", "/v1/jobs/{id}", {"id": job_id})
            if not isinstance(last, JsonResponse):
                raise VeilleTransportError("The job endpoint did not return JSON.", TypeError())
            if on_progress is not None:
                on_progress(last.data)
            if _is_terminal(last.data):
                return last
            if time.monotonic() - started + interval > timeout:
                raise VeilleJobTimeoutError(job_id, last)
            await asyncio.sleep(interval)
            interval = _next_interval(interval)

    async def aclose(self) -> None:
        """Close transport resources owned by this client."""

        if self._closed:
            return
        try:
            if self._owns_http_client:
                await self._http_client.aclose()
        finally:
            self._closed = True

    async def __aenter__(self) -> Self:
        self._ensure_open()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def _call(
        self, name: str, params: dict[str, Any], options: RequestOptions | None
    ) -> APIResponse:
        return await self._send(_prepare_operation(self._configuration, name, params, options))

    async def _send(self, prepared: _PreparedRequest) -> APIResponse:
        self._ensure_open()
        attempt = 0
        while True:
            try:
                response = await self._http_client.request(
                    prepared.method,
                    prepared.url,
                    headers=prepared.headers,
                    content=prepared.content,
                    timeout=prepared.timeout,
                    follow_redirects=False,
                )
                body = await response.aread()
            except httpx.TimeoutException as cause:
                raise VeilleTransportError("Veille request timed out.", cause) from cause
            except Exception as cause:
                if attempt < prepared.max_retries:
                    await asyncio.sleep(
                        _retry_delay(self._configuration.retry_delay, attempt, None)
                    )
                    attempt += 1
                    continue
                raise VeilleTransportError(
                    "Veille request failed before an HTTP response body was received.", cause
                ) from cause
            raw_response = create_raw_response(response, body)
            if _is_retryable(raw_response) and attempt < prepared.max_retries:
                retry_after = (raw_response.headers.get("retry-after") or (None,))[0]
                await asyncio.sleep(
                    _retry_delay(self._configuration.retry_delay, attempt, retry_after)
                )
                attempt += 1
                continue
            return _decode(raw_response, prepared)

    def _ensure_open(self) -> None:
        if self._closed:
            raise VeilleConfigurationError("This AsyncVeilleClient is closed.")


def _build_configuration(
    api_key: str | None,
    base_url: str | None,
    timeout: float | None,
    headers: Mapping[str, str] | None,
    max_retries: int = MAX_RETRIES,
    retry_delay: float = DEFAULT_RETRY_DELAY,
) -> _Configuration:
    key = api_key if api_key is not None else os.environ.get(API_KEY_ENVIRONMENT_VARIABLE)
    if not isinstance(key, str) or not key.strip():
        raise VeilleConfigurationError(
            f"A non-blank Veille API key is required. Pass api_key or set {API_KEY_ENVIRONMENT_VARIABLE}."
        )
    if any(ch in key for ch in "\r\n"):
        raise VeilleConfigurationError("The Veille API key cannot be used in an HTTP header.")
    url = (base_url or DEFAULT_BASE_URL).rstrip("/")
    parts = urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        raise VeilleConfigurationError("base_url must be an absolute http or https URL.")
    if timeout is not None and (not isinstance(timeout, (int, float)) or timeout <= 0):
        raise VeilleConfigurationError("timeout must be a positive number of seconds or None.")
    if isinstance(max_retries, bool) or not isinstance(max_retries, int) or max_retries < 0:
        raise VeilleConfigurationError("max_retries must be a non-negative integer.")
    if not isinstance(retry_delay, (int, float)) or retry_delay < 0:
        raise VeilleConfigurationError("retry_delay must be a non-negative number of seconds.")
    return _Configuration(
        api_key=key,
        base_url=url,
        timeout=timeout,
        headers=dict(headers or {}),
        max_retries=max_retries,
        retry_delay=float(retry_delay),
    )


def _prepare_operation(
    configuration: _Configuration,
    name: str,
    params: Mapping[str, Any],
    options: RequestOptions | None,
) -> _PreparedRequest:
    endpoint = ENDPOINTS[name]
    method = (options.method if options else None) or endpoint.methods[0]
    if method not in endpoint.methods:
        raise VeilleConfigurationError(
            f"{endpoint.path} supports {', '.join(endpoint.methods)}, not {method}."
        )
    for required in endpoint.required:
        if params.get(required) is None:
            raise VeilleSerializationError(f'The "{required}" parameter is required.', required)
    return _prepare(configuration, method, endpoint.path, params, options, endpoint.response)


def _prepare(
    configuration: _Configuration,
    method: HTTPMethod,
    path: str,
    params: Mapping[str, Any] | None,
    options: RequestOptions | None,
    expected: Literal["json", "any"],
) -> _PreparedRequest:
    if method not in ("GET", "POST"):
        raise VeilleConfigurationError(f"Unsupported HTTP method: {method!r}.")
    if not isinstance(path, str) or not path.startswith("/"):
        raise VeilleConfigurationError('The request path must start with "/".')
    serialized = serialize_request(method, path, params)
    url = configuration.base_url + serialized.path
    if serialized.query:
        url += "?" + encode_query(serialized.query)
    headers = {
        "Accept": "application/json, */*;q=0.8",
        "User-Agent": f"veille-python/{__version__}",
        **configuration.headers,
        **dict((options.headers if options else None) or {}),
        "x-api-key": configuration.api_key,
    }
    content = None
    if serialized.body is not None:
        headers["Content-Type"] = "application/json"
        content = encode_json_body(serialized.body)
    timeout = options.timeout if options and options.timeout is not None else configuration.timeout
    max_retries = (
        options.max_retries
        if options and options.max_retries is not None
        else configuration.max_retries
    )
    return _PreparedRequest(method, url, headers, content, timeout, expected, max_retries)


def _decode(raw_response: RawResponse, prepared: _PreparedRequest) -> APIResponse:
    if not 200 <= raw_response.status <= 299:
        raise create_api_error(raw_response)
    return decode_success_response(raw_response, prepared.expected)


def _check_concurrency(concurrency: int) -> None:
    if isinstance(concurrency, bool) or not isinstance(concurrency, int) or concurrency < 1:
        raise VeilleConfigurationError("concurrency must be a positive integer.")


def _settle(index: int, future: Future[_T]) -> BatchResult[_T]:
    error = future.exception()
    if error is not None:
        return BatchResult(index=index, error=error)
    return BatchResult(index=index, value=future.result())


def _is_retryable(raw_response: RawResponse) -> bool:
    """Server errors and plan rate limits (401/429 "Rate limit exceeded") are retried; per-key quotas are not."""

    if raw_response.status in RETRYABLE_STATUSES:
        return True
    if raw_response.status not in (401, 429):
        return False
    message = (create_api_error(raw_response).error_message or "").lower()
    if "quota" in message:
        return False
    return "rate limit" in message or (raw_response.status == 429 and not message)


def _retry_delay(base: float, attempt: int, retry_after: str | None) -> float:
    if retry_after is not None:
        try:
            seconds = float(retry_after)
        except ValueError:
            seconds = -1.0
        if seconds >= 0:
            return min(seconds, 60.0)
    return float(min(base * RETRY_BACKOFF_FACTOR**attempt, MAX_RETRY_DELAY))


def _check_job_id(job_id: str) -> None:
    if not isinstance(job_id, str) or not job_id.strip():
        raise VeilleSerializationError("A non-blank job id is required.", "id")


def _is_terminal(job: Any) -> bool:
    return isinstance(job, dict) and job.get("status") in JOB_TERMINAL_STATUSES


def _next_interval(interval: float) -> float:
    return max(interval, min(interval * 1.5, MAX_POLL_INTERVAL))
