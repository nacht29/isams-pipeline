import json
from google.cloud import secretmanager
from typing import Any, Dict


def get_secret(secret_id: str, project_id: str, credentials) -> Dict[str, Any]:
    """Fetch a secret from Google Secret Manager.

    Args:
        secret_id: ID of the secret in Secret Manager.
        project_id: GCP project ID where the secret is stored.
        credentials: Credentials used to authenticate with GCP.

    Returns:
        The secret payload parsed as JSON.
    """
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return json.loads(payload)
