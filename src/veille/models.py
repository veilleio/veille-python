"""Public response and option types."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, Generic, Literal, TypeAlias, TypeVar

T = TypeVar("T")

HTTPMethod: TypeAlias = Literal["GET", "POST"]


@dataclass(frozen=True, slots=True)
class RawResponse:
    """Buffered HTTP response: status, lower-cased multi-value headers, content type and body bytes."""

    status: int
    status_text: str
    headers: Mapping[str, tuple[str, ...]]
    content_type: str | None
    body: bytes = field(repr=False)


@dataclass(frozen=True, slots=True)
class JsonResponse:
    """A successful JSON response; ``data`` is the parsed body."""

    data: Any
    raw_response: RawResponse = field(repr=False)
    kind: Literal["json"] = "json"


@dataclass(frozen=True, slots=True)
class BinaryResponse:
    """A successful non-JSON response (image, PDF, HTML…)."""

    bytes: bytes = field(repr=False)
    content_type: str | None = None
    raw_response: RawResponse | None = field(default=None, repr=False)
    kind: Literal["binary"] = "binary"


APIResponse: TypeAlias = JsonResponse | BinaryResponse


@dataclass(frozen=True, slots=True)
class RequestOptions:
    """Per-request options for generated endpoint methods."""

    method: HTTPMethod | None = None
    """GET (default when supported) sends query parameters; POST sends a JSON body."""
    timeout: float | None = None
    """Seconds; overrides the client timeout for this request."""
    headers: Mapping[str, str] | None = None
    """Extra headers for this request."""
    max_retries: int | None = None
    """Overrides the client retry count for this request (0 disables retries)."""


@dataclass(frozen=True, slots=True)
class BatchResult(Generic[T]):
    """Outcome of one ``batch()`` item: ``value`` when ``ok``, else ``error``."""

    index: int
    value: T | None = None
    error: BaseException | None = None

    @property
    def ok(self) -> bool:
        return self.error is None


@dataclass(frozen=True, slots=True)
class EndpointDefinition:
    """Path, supported methods and required parameters of one documented operation."""

    path: str
    methods: tuple[HTTPMethod, ...]
    response: Literal["json", "any"]
    required: tuple[str, ...]
