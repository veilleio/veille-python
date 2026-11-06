"""Official Python SDK for the Veille API."""

from ._endpoints import ENDPOINTS
from ._version import __version__
from .client import (
    DEFAULT_BASE_URL,
    DEFAULT_CONCURRENCY,
    DEFAULT_RETRY_DELAY,
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    RETRY_BACKOFF_FACTOR,
    AsyncVeilleClient,
    VeilleClient,
)
from .errors import (
    VeilleAPIError,
    VeilleConfigurationError,
    VeilleError,
    VeilleJobTimeoutError,
    VeilleResponseDecodingError,
    VeilleSerializationError,
    VeilleTransportError,
)
from .models import (
    APIResponse,
    BatchResult,
    BinaryResponse,
    EndpointDefinition,
    HTTPMethod,
    JsonResponse,
    RawResponse,
    RequestOptions,
)

__all__ = [
    "APIResponse",
    "AsyncVeilleClient",
    "BatchResult",
    "BinaryResponse",
    "DEFAULT_BASE_URL",
    "DEFAULT_CONCURRENCY",
    "DEFAULT_RETRY_DELAY",
    "DEFAULT_TIMEOUT",
    "MAX_RETRIES",
    "RETRY_BACKOFF_FACTOR",
    "ENDPOINTS",
    "EndpointDefinition",
    "HTTPMethod",
    "JsonResponse",
    "RawResponse",
    "RequestOptions",
    "VeilleAPIError",
    "VeilleClient",
    "VeilleConfigurationError",
    "VeilleError",
    "VeilleJobTimeoutError",
    "VeilleResponseDecodingError",
    "VeilleSerializationError",
    "VeilleTransportError",
    "__version__",
]
