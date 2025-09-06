# isams-pipeline

A demonstration on building a data pipeline that moves data from iSAMS API endpoints to BigQuery.

## High-level Architecture

![alt text](image.png)

**Explanation:**
1. A scheduler in the Compute Engine Instance triggers `iSAMS.py`.
2. The script pulls OAuth2 creds from Secret Manager.
3. The script sends HTTP requests to iSAMS API endpoints and receive data payloads in the form of JSON strings.
4. The payloads are processed with Python and loaded to BigQuery.
5. You can further model the data in BigQuery.

---

## Set Up

### Prerequisites
1. GCP project with BigQuery and Secret Manager enabled
2. iSAMS API OAuth2 client credentials:
	- client ID
	- client secret
3. iSAMS API endpoints:
	- base URL
	- endpoint URLS
4. Service account with BigQuery + Secret Manager access
5. Python 3.11+

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

### Python dependencies
1. Create and activate a Python virtual environment (venv) to install dependencies.

	```bash
	python3 -m venv myvenv
	source myvenv/bin/activate
	```

2. Install the dependencies
	```bash
	pip install --upgrade dask pandas pandas-gbq numpy openpyxl xlsxwriter xlrd db-dtypes SQLAlchemy
	pip install --upgrade google-api-python-client pydrive
	pip install --upgrade google-cloud-bigquery google-cloud-storage google-cloud-bigquery-storage
	pip install --upgrade google-cloud-secret-manager google-auth google-auth-oauthlib google-auth-httplib2
	pip install --upgrade colorama
	```
---

## Execution

### Credentials configuration
1. Include service account credentials: modify this part in `iSAMS.py`:
	- `KEY_PATH`: path to the directory that contains your service account key.
	- `KEY_NAME`: name of the service account key.
	- This set up allows you to store and use multiple keys.
	```python
	# Service Account Credentials
	KEY_PATH = "Path to folder containing Service Account Keys"
	KEY_NAME = 'Service Account JSON key file'
	SERVICE_ACC_KEY = f'{KEY_PATH}/{KEY_NAME}'
	```

2. Create a service account credentials object. This allows you to access resources the service account is granted permission to.
	```py
	# retrieve Service Account credentials
	service_acc_creds = service_account.Credentials.from_service_account_file(SERVICE_ACC_KEY)
	```

3. Retrieve OAuth2 client credentials from Secret Manager. This allows the script to send HTTP requests to iSAMS API endpoints.
	```py
	# retrieve Service Account credentials
	service_acc_creds = service_account.Credentials.from_service_account_file(SERVICE_ACC_KEY)

	# retrieve OAuth2 client credentials from Secret Manager
	SECRET_ID = "isams_api_credentials"
	secret_payload = get_secret(SECRET_ID, service_acc_creds.project_id, service_acc_creds)

	# Set OAuth2 client credentials
	CLIENT_ID = secret_payload["CLIENT_ID"]
	CLIENT_SECRET = secret_payload["CLIENT_SECRET"]
	TOKEN_URL = secret_payload["TOKEN_URL"]
	API_BASE_URL = secret_payload["API_BASE_URL"]
	```

4. Build a BigQuery client object to allow your script to communicate with BigQuery.
	```py
	# build BigQuery API Client
	bq_client = bq.Client(credentials=service_acc_creds, project=service_acc_creds.project_id)
	```

### Pipeline configuration
1. `python_utils.formats.py`:

	```py
	isams_dataset_endpoints = {
		'students': {
			'url': '/api/students',
			'object': 'students',
			'pages': 'multi-page',
			'table_id': 'project_id.dataset.students',
			'schema': students_schema,
		},
		
		'school_terms': {
			'url': '/api/school/terms',
			'object': 'terms',
			'pages': 'single-page',
			'table_id': 'project_id.dataset.school_terms',
			'schema': school_terms_schema
		},
		
		'year_groups' : {
			'url': '/api/school/yeargroups',
			'object': 'yearGroups',
			'pages': 'single-page',
			'table_id': 'project_id.dataset.year_groups',
			'schema': year_groups_schema
		}
	}
	```

- Map iSAMS endpoints to BigQuery tables in `custom.py` and `python_utils/formats.py`.
- Tweak transformation helpers in `python_utils/modify_cols.py` if the raw fields need a polish.

### Run it
```bash
python iSAMS.py
```

---

## Scheduling

```bash
placeholder
```

---

## Custom Pipelines

`custom.py` includes an example: `year_group_division` and a `custom_pipelines()` hook. Use this spot for add-on workflows or experimental endpoints.

---

## Alternatives

Once you have finished your pipeline configurations, consider dockerising the script and use Cron or any other scheduler to run the docker image.