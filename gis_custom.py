import sys
import functools
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from google.cloud import storage, bigquery as bq
from colorama import Fore, Back, Style
from secret_manager import get_secret

sys.path.append("/home/working_directory")
from python_utils.bigquery import *
from python_utils.utils import *
from python_utils.formats import *
from python_utils.json import *
from python_utils.modify_cols import *

# force flushing for logs
sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = open(sys.stderr.fileno(), 'w', buffering=1)
print = functools.partial(print, flush=True)
PYTHONUNBUFFERED = True

# GCP Creds
KEY_PATH = "Path to folder containing Service Account Keys"
KEY_NAME = 'Service Account JSON key file'
SERVICE_ACC_KEY = f'{KEY_PATH}/{KEY_NAME}'

service_acc_creds = service_account.Credentials.from_service_account_file(SERVICE_ACC_KEY)
bq_client = bq.Client(credentials=service_acc_creds, project=service_acc_creds.project_id)

# iSAMS creds from Secret Manager
SECRET_ID = "isams_api_credentials"
secret_payload = get_secret(SECRET_ID, service_acc_creds.project_id, service_acc_creds)
CLIENT_ID = secret_payload["CLIENT_ID"]
CLIENT_SECRET = secret_payload["CLIENT_SECRET"]
TOKEN_URL = secret_payload["TOKEN_URL"]
API_BASE_URL = secret_payload["API_BASE_URL"]

def year_group_division():
	access_token = gen_access_token(TOKEN_URL, CLIENT_ID, CLIENT_SECRET, API_BASE_URL)
	for id in range(-2, 14+1):
		api_response = api_get(access_token, api_url=f'{API_BASE_URL}/api/school/yeargroups/{id}/divisions', content_type='application/json')
		endpoint_object = api_response['divisions']
		
		cur_df = pd.DataFrame(endpoint_object)
		cur_df['year_group_id'] = id
		
		print(cur_df)
		df_to_bq(
			bq_client=bq_client,
			df=cur_df,
			table_id='taylors-data-poc.isams_data.divisions',
			mode='t' if id == -2 else 'a',
			autodetect=True
		)

def custom_pipelines():
	year_group_division()

if __name__ == '__main__':
	custom_pipelines()