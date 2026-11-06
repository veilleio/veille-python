# Examples

```sh
pip install veille
export VEILLE_API_KEY="YOUR_API_KEY"
python examples/json_response.py
```

- `json_response.py` — call the featured endpoint and print the JSON result.
- `async_client.py` — use `AsyncVeilleClient`.
- `any_endpoint.py` — call any path with `request()` and handle API errors.
- `wait_for_job.py` — start an async job and wait for its result.
