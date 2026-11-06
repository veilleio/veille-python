"""Generated from the Veille OpenAPI document. Do not edit by hand."""

from __future__ import annotations

from .models import EndpointDefinition

ENDPOINTS: dict[str, EndpointDefinition] = {
    "intelligence_domain": EndpointDefinition(
        path="/v1/intelligence/domain",
        methods=("GET",),
        response="json",
        required=("query",),
    ),
    "intelligence_email": EndpointDefinition(
        path="/v1/intelligence/email",
        methods=("GET",),
        response="json",
        required=("query",),
    ),
    "intelligence_emailq": EndpointDefinition(
        path="/v1/intelligence/emailq",
        methods=("GET",),
        response="json",
        required=("query",),
    ),
    "intelligence_ip": EndpointDefinition(
        path="/v1/intelligence/ip",
        methods=("GET",),
        response="json",
        required=("query",),
    ),
    "intelligence_phone": EndpointDefinition(
        path="/v1/intelligence/phone",
        methods=("GET",),
        response="json",
        required=("query",),
    ),
    "jobs": EndpointDefinition(
        path="/v1/jobs/{id}",
        methods=("GET",),
        response="json",
        required=("id",),
    ),
    "stats": EndpointDefinition(
        path="/v1/stats",
        methods=("GET",),
        response="json",
        required=(),
    ),
    "usage": EndpointDefinition(
        path="/v1/usage",
        methods=("GET",),
        response="json",
        required=(),
    ),
    "vat": EndpointDefinition(
        path="/v1/vat",
        methods=("GET",),
        response="json",
        required=("query",),
    ),
    "vat_iban": EndpointDefinition(
        path="/v1/vat/iban",
        methods=("GET",),
        response="json",
        required=("query",),
    ),
    "vat_rates": EndpointDefinition(
        path="/v1/vat/rates",
        methods=("GET",),
        response="json",
        required=(),
    ),
}
