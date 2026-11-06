"""Start an async job and wait for its result."""

from veille import VeilleClient

with VeilleClient() as client:  # reads VEILLE_API_KEY
    submitted = client.intelligence_email(query="jane.doe@example.com", is_async=True)
    job = client.wait_for_job(
        submitted.data["job_id"],
        on_progress=lambda j: print(j["status"], j.get("progress")),
    )
    print(job.data)
