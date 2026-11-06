# Veille Python SDK

The official Python SDK for the [Veille](https://www.veille.io) fraud prevention API.

Validate emails, domains, IPs, VAT numbers and IBANs in milliseconds to block fake sign-ups, bots and fraud.

The SDK exposes **11 typed methods**, one per documented endpoint, with blocking and `asyncio` clients built on [HTTPX](https://www.python-httpx.org/), plus a generic `request()`.

## Requirements

- Python 3.11 or newer

## Installation

```sh
pip install veille
```

## Get your API key

[Sign up for Veille](https://app.veille.io/register) or sign in, then copy your API key from the [dashboard](https://app.veille.io). The client reads the `VEILLE_API_KEY` environment variable when no key is passed.

## Quick start

```python
import os

from veille import VeilleClient

with VeilleClient(os.environ["VEILLE_API_KEY"]) as client:
    response = client.intelligence_email(query="jane.doe@example.com")
    print(response.data)
```

Keyword arguments mirror the [API reference](https://app.veille.io/openapi). Python keywords get a trailing underscore (`from_=`), and the wire name is used on the request.

## Async jobs

Any call accepts `is_async: true` (useful past the 60-second server limit): the response is then a `job_id`. `wait_for_job()` polls `GET /v1/jobs/{id}` until the job reaches a terminal status (`CompletedJob`, `Error`, `NotFound`, `BadRequest`):

```python
submitted = client.intelligence_email(query="jane.doe@example.com", is_async=True)
job = client.wait_for_job(
    submitted.data["job_id"],
    on_progress=lambda j: print(j["status"], j.get("progress")),
)
print(job.data)
```

## Async I/O

```python
import asyncio

from veille import AsyncVeilleClient


async def main() -> None:
    async with AsyncVeilleClient() as client:
        response = await client.intelligence_email(query="jane.doe@example.com")
        print(response.data)


asyncio.run(main())
```

## GET or POST

Methods use GET when the endpoint supports it (parameters in the query string). POST sends the same parameters as a JSON body:

`None` values are omitted, `False` and `0` are sent, and sequences repeat the parameter name.

## Any endpoint

```python
response = client.request("GET", "/v1/usage")
```

## Errors

```python
from veille import VeilleAPIError

try:
    client.intelligence_email(query="jane.doe@example.com")
except VeilleAPIError as error:
    print(error.status, error, error.response_body)
```

| Error | When |
| --- | --- |
| `VeilleConfigurationError` | Missing API key, invalid options, unsupported method, closed client. |
| `VeilleSerializationError` | A required parameter is missing or a value can't be sent. |
| `VeilleTransportError` | Network failure or timeout. |
| `VeilleAPIError` | Non-2xx status (`status`, `error_message`, `response_body`, `raw_response`). |
| `VeilleResponseDecodingError` | A success response could not be decoded. |

All of them extend `VeilleError`.

## Retries

Requests are retried up to 3 times after a network error, a `408`, `500`, `502`, `503` or `504`, or a rate limit — which the API returns as `401` (or `429`) with a `Rate limit exceeded` message. Per-key quota errors (`…: quota daily`) are not retried, nor are `400`, `402`, `404` or client-side timeouts. The delay starts at 1 second and grows 1.5× per retry (capped at 30 seconds); a `Retry-After` header wins.

```python
client = VeilleClient(max_retries=5, retry_delay=0.5)

# or for one request
client.intelligence_email(query="jane.doe@example.com", request_options=RequestOptions(max_retries=0))
```

## Batch requests

`batch()` runs a function per item on 10 threads (`concurrency`) and returns one `BatchResult` per item, in input order. A failing item never stops the others. `AsyncVeilleClient.batch()` does the same with `asyncio`.

```python
inputs = ["jane.doe@example.com", "john@mailinator.com", "contact@veille.io"]
results = client.batch(inputs, lambda query: client.intelligence_email(query=query), concurrency=5)

for result in results:
    if result.ok:
        print(result.value.data)
    else:
        print(inputs[result.index], result.error)
```

| Constant | Default | Description |
| --- | --- | --- |
| `DEFAULT_CONCURRENCY` | `10` | Tasks run at the same time by batch |
| `DEFAULT_TIMEOUT` | `120.0` | Request timeout (seconds) |
| `MAX_RETRIES` | `3` | Retry attempts after a network error, a 408/5xx or a rate limit |
| `RETRY_BACKOFF_FACTOR` | `1.5` | Exponential backoff multiplier |
| `DEFAULT_RETRY_DELAY` | `1.0` | Delay before the first retry (seconds) |

## Timeouts and custom HTTPX clients

```python
import httpx

from veille import VeilleClient, RequestOptions

client = VeilleClient(timeout=60)  # seconds, default 120, None disables
client.intelligence_email(query="jane.doe@example.com", request_options=RequestOptions(timeout=30))

# Bring your own HTTPX client (proxies, limits, event hooks…). You keep ownership of it.
http_client = httpx.Client(proxy="http://localhost:8080")
client = VeilleClient(http_client=http_client)
```

## Endpoints

11 methods, generated from the [OpenAPI document](https://app.veille.io/openapi).

| Method | HTTP | Description |
| --- | --- | --- |
| `intelligence_domain()` | GET `/v1/intelligence/domain` | Check any domain instantly. Detects disposable email providers, public webmail, relay services, and education domains. Returns DNS health w… |
| `intelligence_email()` | GET `/v1/intelligence/email` | Validate any email address in a single call. Detects disposable and temporary inboxes, identifies role accounts, public webmail, relay serv… |
| `intelligence_emailq()` | GET `/v1/intelligence/emailq` | Deep email deliverability verification. Performs full Email Validation plus SMTP inbox check, catch-all detection, and returns a qualificat… |
| `intelligence_ip()` | GET `/v1/intelligence/ip` | Assess the reputation of any IP address. Detects VPNs, proxies, Tor exit nodes, datacenter hosting, abusive traffic, and bots. Returns geol… |
| `intelligence_phone()` | GET `/v1/intelligence/phone` | Validate any phone number in E.164 format. Detects disposable and virtual numbers, identifies carrier and line type (mobile/fixed/VoIP), re… |
| `jobs()` | GET `/v1/jobs/{id}` | Poll the status, progress (0–100) and result of a job started with is_async=true. Polling is free. Poll until status is terminal: Completed… |
| `stats()` | GET `/v1/stats` | Infrastructure health for an engine or endpoint over the last hour. Not scoped to your account or tenant. Enabled per account: HTTP 403 mea… |
| `usage()` | GET `/v1/usage` | Retrieve real-time usage statistics and credit balance for your Veille account. |
| `vat()` | GET `/v1/vat` | Validate a European VAT number against the VIES database. Returns company name, registered address, and validity status for any EU member s… |
| `vat_iban()` | GET `/v1/vat/iban` | Validate any IBAN and retrieve associated bank details. Returns the BIC/SWIFT code, bank name, country, BBAN structural breakdown, and SEPA… |
| `vat_rates()` | GET `/v1/vat/rates` | Get current ECB exchange rates for any supported base currency. Optionally filter to specific target currencies. Updated daily from the Eur… |

## All Veille SDKs

| SDK | Package | Install |
| --- | --- | --- |
| Node.js | [`@veilleio/sdk`](https://www.npmjs.com/package/@veilleio/sdk) | `npm install @veilleio/sdk` |
| Python | [`veille`](https://pypi.org/project/veille/) | `pip install veille` |
| Go | [`veille-go`](https://pkg.go.dev/github.com/veilleio/veille-go) | `go get github.com/veilleio/veille-go` |
| .NET | [`Veille`](https://www.nuget.org/packages/Veille) | `dotnet add package Veille` |
| Ruby | [`veille`](https://rubygems.org/gems/veille) | `gem install veille` |
| PHP | [`veille/sdk`](https://packagist.org/packages/veille/sdk) | `composer require veille/sdk` |
| Java | [`veille-java`](https://github.com/veilleio/veille-java) | build from source, see its README |
| CLI | [`@veilleio/cli`](https://www.npmjs.com/package/@veilleio/cli) | `npm install -g @veilleio/cli` |
| MCP server | [`@veilleio/mcp`](https://www.npmjs.com/package/@veilleio/mcp) | `npx -y @veilleio/mcp` |

## License

MIT — see [LICENSE](LICENSE).
