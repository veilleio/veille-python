"""Generated from the Veille OpenAPI document. Do not edit by hand."""

from __future__ import annotations

from typing import Any, cast

from .models import APIResponse, JsonResponse, RequestOptions


class _SyncOperations:
    """Generated Veille endpoint methods."""

    __slots__ = ()

    def _call(
        self, name: str, params: dict[str, Any], options: RequestOptions | None
    ) -> APIResponse:
        raise NotImplementedError

    def intelligence_domain(
        self,
        *,
        query: str,
        certificate_transparency: bool | None = None,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Domain Validation. Check any domain instantly. Detects disposable email providers, public webmail, relay services, and education domains. Returns DNS health with MX provider detection, domain history, and optional SSL/TLS certificate transparency. Credit cost: 2 credits per call.

        ``GET /v1/intelligence/domain``

        Args:
            query: The domain to validate. Accepts raw domains (tempmail.org), full URLs (https://www.tempmail.org/page), or domains with www. prefix, all are normalized automatically.
            certificate_transparency: Enable Certificate Transparency lookup. Returns SSL/TLS certificate history, current certificate, issuers, and all Subject Alternative Names (SANs) ever associated with the domain. Adds 1-5 seconds o…
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            self._call(
                "intelligence_domain",
                {
                    "query": query,
                    "certificate_transparency": certificate_transparency,
                    "fields": fields,
                    "is_async": is_async,
                    "soft_fail": soft_fail,
                },
                request_options,
            ),
        )

    def intelligence_email(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Email Validation. Validate any email address in a single call. Detects disposable and temporary inboxes, identifies role accounts, public webmail, relay services, and returns a 0-100 risk score. For deep deliverability verification (SMTP check, catch-all de… Credit cost: 3 credits per call.

        ``GET /v1/intelligence/email``

        Args:
            query: The email address to validate (e.g. john@example.com). Automatically normalized to lowercase.
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            self._call(
                "intelligence_email",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    def intelligence_emailq(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Email Qualification. Deep email deliverability verification. Performs full Email Validation plus SMTP inbox check, catch-all detection, and returns a qualification verdict (valid, invalid, risky, disposable, unknown). Credit cost: 5 credits per call.

        ``GET /v1/intelligence/emailq``

        Args:
            query: The email address to qualify (e.g. john@example.com). Automatically normalized to lowercase.
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            self._call(
                "intelligence_emailq",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    def intelligence_ip(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """IP Reputation. Assess the reputation of any IP address. Detects VPNs, proxies, Tor exit nodes, datacenter hosting, abusive traffic, and bots. Returns geolocation, network owner, and a 0-100 threat score. Credit cost: 2 credits per call.

        ``GET /v1/intelligence/ip``

        Args:
            query: The IP address to analyze (IPv4 or IPv6).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            self._call(
                "intelligence_ip",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    def intelligence_phone(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Phone Validation. Validate any phone number in E.164 format. Detects disposable and virtual numbers, identifies carrier and line type (mobile/fixed/VoIP), returns country and timezone, and computes a 0-100 risk score. Credit cost: 1 credit per call.

        ``GET /v1/intelligence/phone``

        Args:
            query: The phone number to validate in E.164 format (must start with +, e.g. +33612345678).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            self._call(
                "intelligence_phone",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    def jobs(
        self,
        *,
        id: str,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Jobs. Poll the status, progress (0–100) and result of a job started with is_async=true. Polling is free. Poll until status is terminal: CompletedJob, Error, NotFound or BadRequest.

        ``GET /v1/jobs/{id}``

        Args:
            id: The job_id returned by an endpoint called with is_async=true.
        """
        return cast(JsonResponse, self._call("jobs", {"id": id}, request_options))

    def stats(
        self,
        *,
        engine: str | None = None,
        path: str | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Stats. Infrastructure health for an engine or endpoint over the last hour. Not scoped to your account or tenant. Enabled per account: HTTP 403 means contact support to activate it.

        ``GET /v1/stats``

        Args:
            engine: API family to check, for example vat. Provide at least engine or path.
            path: Specific endpoint to check, for example /v1/vat. If you also pass engine, use an endpoint from that API.
        """
        return cast(
            JsonResponse, self._call("stats", {"engine": engine, "path": path}, request_options)
        )

    def usage(
        self,
        *,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Usage. Retrieve real-time usage statistics and credit balance for your Veille account.

        ``GET /v1/usage``
        """
        return cast(JsonResponse, self._call("usage", {}, request_options))

    def vat(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """VAT Validation. Validate a European VAT number against the VIES database. Returns company name, registered address, and validity status for any EU member state. Credit cost: 1 credit per call.

        ``GET /v1/vat``

        Args:
            query: The VAT number to validate (e.g. FR40303265045).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            self._call(
                "vat",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    def vat_iban(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """IBAN Validation. Validate any IBAN and retrieve associated bank details. Returns the BIC/SWIFT code, bank name, country, BBAN structural breakdown, and SEPA zone membership. Credit cost: 1 credit per call.

        ``GET /v1/vat/iban``

        Args:
            query: The IBAN to validate (e.g. FR7630006000011234567890189).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            self._call(
                "vat_iban",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    def vat_rates(
        self,
        *,
        base: str | None = None,
        symbols: str | None = None,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Exchange Rates. Get current ECB exchange rates for any supported base currency. Optionally filter to specific target currencies. Updated daily from the European Central Bank. Credit cost: 1 credit per call.

        ``GET /v1/vat/rates``

        Args:
            base: Base currency ISO 4217 code (defaults to EUR).
            symbols: Comma-separated target currency codes to filter (e.g. USD,GBP,JPY).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            self._call(
                "vat_rates",
                {
                    "base": base,
                    "symbols": symbols,
                    "fields": fields,
                    "is_async": is_async,
                    "soft_fail": soft_fail,
                },
                request_options,
            ),
        )


class _AsyncOperations:
    """Generated Veille endpoint methods."""

    __slots__ = ()

    async def _call(
        self, name: str, params: dict[str, Any], options: RequestOptions | None
    ) -> APIResponse:
        raise NotImplementedError

    async def intelligence_domain(
        self,
        *,
        query: str,
        certificate_transparency: bool | None = None,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Domain Validation. Check any domain instantly. Detects disposable email providers, public webmail, relay services, and education domains. Returns DNS health with MX provider detection, domain history, and optional SSL/TLS certificate transparency. Credit cost: 2 credits per call.

        ``GET /v1/intelligence/domain``

        Args:
            query: The domain to validate. Accepts raw domains (tempmail.org), full URLs (https://www.tempmail.org/page), or domains with www. prefix, all are normalized automatically.
            certificate_transparency: Enable Certificate Transparency lookup. Returns SSL/TLS certificate history, current certificate, issuers, and all Subject Alternative Names (SANs) ever associated with the domain. Adds 1-5 seconds o…
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            await self._call(
                "intelligence_domain",
                {
                    "query": query,
                    "certificate_transparency": certificate_transparency,
                    "fields": fields,
                    "is_async": is_async,
                    "soft_fail": soft_fail,
                },
                request_options,
            ),
        )

    async def intelligence_email(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Email Validation. Validate any email address in a single call. Detects disposable and temporary inboxes, identifies role accounts, public webmail, relay services, and returns a 0-100 risk score. For deep deliverability verification (SMTP check, catch-all de… Credit cost: 3 credits per call.

        ``GET /v1/intelligence/email``

        Args:
            query: The email address to validate (e.g. john@example.com). Automatically normalized to lowercase.
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            await self._call(
                "intelligence_email",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    async def intelligence_emailq(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Email Qualification. Deep email deliverability verification. Performs full Email Validation plus SMTP inbox check, catch-all detection, and returns a qualification verdict (valid, invalid, risky, disposable, unknown). Credit cost: 5 credits per call.

        ``GET /v1/intelligence/emailq``

        Args:
            query: The email address to qualify (e.g. john@example.com). Automatically normalized to lowercase.
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            await self._call(
                "intelligence_emailq",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    async def intelligence_ip(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """IP Reputation. Assess the reputation of any IP address. Detects VPNs, proxies, Tor exit nodes, datacenter hosting, abusive traffic, and bots. Returns geolocation, network owner, and a 0-100 threat score. Credit cost: 2 credits per call.

        ``GET /v1/intelligence/ip``

        Args:
            query: The IP address to analyze (IPv4 or IPv6).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            await self._call(
                "intelligence_ip",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    async def intelligence_phone(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Phone Validation. Validate any phone number in E.164 format. Detects disposable and virtual numbers, identifies carrier and line type (mobile/fixed/VoIP), returns country and timezone, and computes a 0-100 risk score. Credit cost: 1 credit per call.

        ``GET /v1/intelligence/phone``

        Args:
            query: The phone number to validate in E.164 format (must start with +, e.g. +33612345678).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            await self._call(
                "intelligence_phone",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    async def jobs(
        self,
        *,
        id: str,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Jobs. Poll the status, progress (0–100) and result of a job started with is_async=true. Polling is free. Poll until status is terminal: CompletedJob, Error, NotFound or BadRequest.

        ``GET /v1/jobs/{id}``

        Args:
            id: The job_id returned by an endpoint called with is_async=true.
        """
        return cast(JsonResponse, await self._call("jobs", {"id": id}, request_options))

    async def stats(
        self,
        *,
        engine: str | None = None,
        path: str | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Stats. Infrastructure health for an engine or endpoint over the last hour. Not scoped to your account or tenant. Enabled per account: HTTP 403 means contact support to activate it.

        ``GET /v1/stats``

        Args:
            engine: API family to check, for example vat. Provide at least engine or path.
            path: Specific endpoint to check, for example /v1/vat. If you also pass engine, use an endpoint from that API.
        """
        return cast(
            JsonResponse,
            await self._call("stats", {"engine": engine, "path": path}, request_options),
        )

    async def usage(
        self,
        *,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Usage. Retrieve real-time usage statistics and credit balance for your Veille account.

        ``GET /v1/usage``
        """
        return cast(JsonResponse, await self._call("usage", {}, request_options))

    async def vat(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """VAT Validation. Validate a European VAT number against the VIES database. Returns company name, registered address, and validity status for any EU member state. Credit cost: 1 credit per call.

        ``GET /v1/vat``

        Args:
            query: The VAT number to validate (e.g. FR40303265045).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            await self._call(
                "vat",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    async def vat_iban(
        self,
        *,
        query: str,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """IBAN Validation. Validate any IBAN and retrieve associated bank details. Returns the BIC/SWIFT code, bank name, country, BBAN structural breakdown, and SEPA zone membership. Credit cost: 1 credit per call.

        ``GET /v1/vat/iban``

        Args:
            query: The IBAN to validate (e.g. FR7630006000011234567890189).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            await self._call(
                "vat_iban",
                {"query": query, "fields": fields, "is_async": is_async, "soft_fail": soft_fail},
                request_options,
            ),
        )

    async def vat_rates(
        self,
        *,
        base: str | None = None,
        symbols: str | None = None,
        fields: str | None = None,
        is_async: bool | None = None,
        soft_fail: bool | None = None,
        request_options: RequestOptions | None = None,
    ) -> JsonResponse:
        """Exchange Rates. Get current ECB exchange rates for any supported base currency. Optionally filter to specific target currencies. Updated daily from the European Central Bank. Credit cost: 1 credit per call.

        ``GET /v1/vat/rates``

        Args:
            base: Base currency ISO 4217 code (defaults to EUR).
            symbols: Comma-separated target currency codes to filter (e.g. USD,GBP,JPY).
            fields: Comma-separated list of fields to keep in the response, with dot notation for nested fields (e.g. name,location.city). Does not change the credit cost.
            is_async: Process the request asynchronously: the response is a job_id to poll on /v1/jobs/{id} (see waitForJob).
            soft_fail: Return HTTP 200 even when an error occurs; the error is then in the response body.
        """
        return cast(
            JsonResponse,
            await self._call(
                "vat_rates",
                {
                    "base": base,
                    "symbols": symbols,
                    "fields": fields,
                    "is_async": is_async,
                    "soft_fail": soft_fail,
                },
                request_options,
            ),
        )
