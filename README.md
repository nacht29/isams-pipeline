# isams-pipeline

A lightweight toolkit for piping data from iSAMS into BigQuery. Use it as-is or bolt on extra pieces for your own flavour of ETL/ELT.

## Architecture

```
+---------------+      +---------------------+      +-----------+
| Cloud Scheduler| --->| Python runtime      | ---> | BigQuery  |
| or cron job    |     | (`iSAMS.py`)    |     | datasets  |
+-------+-------+      |  ↓ secrets       |      +-----------+
        |              |  Secret Manager     |
        |              +----------+----------+
        |                         |
        |                         v
        |                 (optional) Cloud Storage
        |
        v
   iSAMS API
```

1. A scheduler triggers `iSAMS.py`.
2. The script pulls OAuth2 creds from Secret Manager.
3. iSAMS endpoints are queried and shaped with `pandas`.
4. Clean data lands in BigQuery.
5. Optional: stash raw files in Cloud Storage.

## Getting Started

### Prerequisites
- GCP project with BigQuery, Secret Manager and (optionally) Cloud Storage enabled
- iSAMS OAuth2 client (client ID/secret, token URL and base API URL)
- Service account with BigQuery + Secret Manager access
- Python 3.11+

### Install dependencies
```bash
git clone <this repo>
cd isams-pipeline
bash install.sh  # installs Google + pandas goodies
```

### Store OAuth2 credentials in Secret Manager

1. This project retrieves OAuth2 client credentials from [Secret Manager](https://cloud.google.com/secret-manager) using the secret ID `isams_api_credentials`. Store the credentials as a JSON payload:

	- Store as `oauth_credentials.json`
	```json
	{
		"CLIENT_ID": "your-client-id",
		"CLIENT_SECRET": "your-client-secret",
		"TOKEN_URL": "https://example.com/oauth/token",
		"API_BASE_URL": "https://example.com/api"
	}
	```

2. Create the secret (or add a new version) using the `gcloud` CLI:

	```bash
	# create the secret from the JSON file
	gcloud secrets create isams_api_credentials --data-file=oauth_credentials.json

	# or, add a new version to an existing secret
	gcloud secrets versions add isams_api_credentials --data-file=oauth_credentials.json
	```

3. Give your service account the `roles/secretmanager.secretAccessor` role so the script can receive the payload using service account credentials.

### Configure the pipeline
- Drop your service account JSON key in the location referenced by `KEY_PATH`/`KEY_NAME` in `iSAMS.py`.
- Map iSAMS endpoints to BigQuery tables in `custom.py` and `python_utils/formats.py`.
- Tweak transformation helpers in `python_utils/modify_cols.py` if the raw fields need a polish.

### Run it
```bash
python iSAMS.py
```
Schedule it via cron, Cloud Scheduler + Cloud Run, or any other runner you fancy.

## Custom pipelines

`custom.py` includes an example (`year_group_division`) and a `custom_pipelines()` hook. Use this spot for add-on workflows or experimental endpoints.
