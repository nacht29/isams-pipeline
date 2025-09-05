# isams-pipeline
Template to create an ETL/ELT pipeline from iSAMS to BigQuery.

## Storing OAuth2 Credentials in Secret Manager

This project retrieves OAuth2 client credentials from [Secret Manager](https://cloud.google.com/secret-manager) using the secret ID `isams_api_credentials`. Store the credentials as a JSON payload with the following structure:

```json
{
  "CLIENT_ID": "your-client-id",
  "CLIENT_SECRET": "your-client-secret",
  "TOKEN_URL": "https://example.com/oauth/token",
  "API_BASE_URL": "https://example.com/api"
}
```

Create the secret (or add a new version) using the `gcloud` CLI:

```bash
# create the secret from the JSON file
gcloud secrets create isams_api_credentials --data-file=oauth_credentials.json

# or, add a new version to an existing secret
gcloud secrets versions add isams_api_credentials --data-file=oauth_credentials.json
```

Ensure the service account running the pipeline has the
`roles/secretmanager.secretAccessor` role for this secret. Screenshots can be
added later to illustrate these steps.
