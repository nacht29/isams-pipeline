import json
from google.cloud import secretmanager
from typing import Any, Dict

def get_secret(secret_id:str, project_id:str, credentials) -> Dict[str, Any]:
	client = secretmanager.SecretManagerServiceClient(credentials=credentials)
	name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
	response = client.access_secret_version(request={"name": name})
	payload = response.payload.data.decode("UTF-8")
	return json.loads(payload)
