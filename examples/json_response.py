"""Call the featured endpoint and print the JSON result."""

import json
import os

from veille import VeilleClient

with VeilleClient(os.environ["VEILLE_API_KEY"]) as client:
    response = client.intelligence_email(query="jane.doe@example.com")
    print(json.dumps(response.data, indent=2))
