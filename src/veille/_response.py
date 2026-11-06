"""Buffered HTTP response preservation and decoding."""

from __future__ import annotations

import json
from types import MappingProxyType
from typing import Any, Literal

import httpx

from .errors import VeilleAPIError, VeilleResponseDecodingError
from .models import APIResponse, BinaryResponse, JsonResponse, RawResponse

_ERROR_MESSAGE_KEYS = ("error", "message", "error_message", "detail")


def create_raw_response(response: httpx.Response, body: bytes) -> RawResponse:
    grouped: dict[str, list[str]] = {}
    for name, value in response.headers.multi_items():
        grouped.setdefault(name.lower(), []).append(value)
    return RawResponse(
        status=response.status_code,
        status_text=response.reason_phrase,
        headers=MappingProxyType({name: tuple(values) for name, values in grouped.items()}),
        content_type=response.headers.get("content-type"),
        body=body,
    )


def create_api_error(raw_response: RawResponse) -> VeilleAPIError:
    parsed, value = _try_parse_json(raw_response.body)
    message = None
    if parsed and isinstance(value, dict):
        for key in _ERROR_MESSAGE_KEYS:
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate:
                message = candidate
                break
    return VeilleAPIError(
        raw_response=raw_response,
        response_body=value if parsed else None,
        error_message=message,
    )


def decode_success_response(
    raw_response: RawResponse, expected: Literal["json", "any"]
) -> APIResponse:
    if not _is_json_media_type(raw_response.content_type):
        if expected == "json":
            raise VeilleResponseDecodingError(
                "Veille returned a successful non-JSON response for a JSON operation.",
                raw_response,
                TypeError(f"Unexpected content type: {raw_response.content_type}."),
            )
        return BinaryResponse(
            bytes=raw_response.body,
            content_type=raw_response.content_type,
            raw_response=raw_response,
        )
    parsed, value = _try_parse_json(raw_response.body)
    if not parsed:
        raise VeilleResponseDecodingError(
            "Veille returned a successful JSON response that could not be decoded.",
            raw_response,
            value if isinstance(value, Exception) else None,
        )
    return JsonResponse(data=value, raw_response=raw_response)


def _is_json_media_type(content_type: str | None) -> bool:
    if content_type is None:
        return False
    media_type = content_type.split(";", 1)[0].strip().lower()
    return media_type == "application/json" or media_type.endswith("+json")


def _try_parse_json(body: bytes) -> tuple[bool, Any]:
    try:
        return True, json.loads(body)
    except (UnicodeDecodeError, json.JSONDecodeError) as cause:
        return False, cause
