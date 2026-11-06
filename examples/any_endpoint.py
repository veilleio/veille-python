"""Call any path with request() and handle API errors."""

from veille import JsonResponse, VeilleAPIError, VeilleClient

with VeilleClient() as client:  # reads VEILLE_API_KEY
    try:
        response = client.request("GET", "/v1/usage")
        if isinstance(response, JsonResponse):
            print(response.data)
    except VeilleAPIError as error:
        print(f"HTTP {error.status}: {error}")
