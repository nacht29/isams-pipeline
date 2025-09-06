import sys
import functools
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
from google.cloud import storage, bigquery as bq
from colorama import Fore, Back, Style

# append the path leading to python_utils, e.g. python_utils is in /home/working_directory/python_utils
sys.path.append("/home/working_directory")
from python_utils.secret_manager import get_secret
from python_utils.bigquery import *
from python_utils.utils import *
from python_utils.formats import *
from python_utils.json import *
from python_utils.modify_cols import *
from custom import *

# force flushing to ensure logs appear in log file immediately during execution
sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = open(sys.stderr.fileno(), 'w', buffering=1)
print = functools.partial(print, flush=True)
PYTHONUNBUFFERED = True

# Service Account Credentials
KEY_PATH = "Path to folder containing Service Account Keys"
KEY_NAME = 'Service Account JSON key file'
SERVICE_ACC_KEY = f'{KEY_PATH}/{KEY_NAME}'

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

# build BigQuery API Client
bq_client = bq.Client(credentials=service_acc_creds, project=service_acc_creds.project_id)

# get the total number of objects in JSON payload from multi-page endpoints
def get_totalCount(access_token:str, full_api_path:str):
	params = {'page': 1, 'pageSize': 1}
	response = api_get(access_token, api_url=full_api_path, content_type=None, params=params)

	try:
		totalCount = response.get('totalCount', 0)
		totalPages = response.get('totalPages', 0)
	except Exception as error:
		print(Fore.RED + f"Failed to get totalCount for '{full_api_path}'\n{error}")
		raise

	if totalCount < 1 or totalPages < 1:
		print(f"Warning! Query is empty for '{full_api_path}'")
		print(f'totalCount = {totalCount}, totalPages = {totalPages}')

	return totalCount

# transform data for each endpoint
def mod_endpoints(endpoint, df:pd.DataFrame):
	match endpoint:
		case 'applicants':
			return applicants_mod(df)
		case 'students':
			return students_mod(df)
		case 'alumni':
			return alumni_mod(df)
		case 'school_terms':
			return school_terms_mod(df)
		case 'year_groups':
			return year_group_mod(df)
		case 'billing_cycles':
			return billing_cycles_mod(df)
	
	return df

# process API endpoints with multiple pages
def multi_page_endpoint(access_token:str, full_api_path:str, endpoint:str, endpoint_info:dict, trunc_flag:bool):
	# get total row count
	totalCount = get_totalCount(access_token, full_api_path)

	# iterate through all pages to extract all data
	print(f'{datetime.now()} start upload')
	cur_page = 1
	page_size = 1000
	while True:
		print(
			Fore.YELLOW
			+ f'Processing {(cur_page * page_size) if (cur_page * page_size) < totalCount else totalCount} out of {totalCount}'
		)

		params = {'page': cur_page, 'pageSize': page_size}
		# API request
		api_response = api_get(access_token, full_api_path, content_type='application/json', params=params)

		# read API response
		# endpoint_object is the data to be extracted from API (list of dicts)
		try:
			endpoint_object = api_response[endpoint_info['object']]
		except Exception as error:
			print(Fore.RED + f"{datetime.now()} Error reading from '{full_api_path}.' Diagnosing...")
			if 'message' in list(api_response.keys()) and api_response['message'] in "The user is not authorised for this request":
				print(Fore.RED + f'Insufficient permission\n\n{error}')
			raise

		# extract API object (dict) and into dataframe
		cur_df = pd.DataFrame(endpoint_object)

		# modify the df
		cur_df = mod_endpoints(endpoint, cur_df)

		# loading
		df_to_bq(
			bq_client=bq_client,
			df=cur_df,
			table_id=endpoint_info['table_id'],
			mode='t' if trunc_flag else 'a',
			schema=endpoint_info['schema'],
			autodetect=True,
		)

		if trunc_flag:
			trunc_flag = False

		print(
			Fore.CYAN
			+ f'Processed {(cur_page * page_size) if (cur_page * page_size) < totalCount else totalCount} out of {totalCount} for {endpoint}'
		)

		# break loop if current iteration already covers all rows
		if cur_page * page_size >= totalCount:
			break
		cur_page += 1
	print(f'{datetime.now()} stop upload')

# process API endpoints with a single page
def single_page_endpoint(access_token:str, full_api_path:str, endpoint:str, endpoint_info:dict, trunc_flag:bool):
	# API request
	api_response = api_get(access_token, full_api_path, content_type='application/json')

	# read API response
	try:
		endpoint_object = api_response[endpoint_info['object']]
	except Exception as error:
		print(Fore.RED + f"{datetime.now()} Error reading from '{full_api_path}.' Diagnosing...")
		if 'message' in list(api_response.keys()) and api_response['message'] in "The user is not authorised for this request":
			print(Fore.RED + f'Insufficient permission\n\n{error}')
		raise

	# extract API object (dict) and into dataframe
	cur_df = pd.DataFrame(endpoint_object)
	# modify the df
	cur_df = mod_endpoints(endpoint, cur_df)

	# loading
	df_to_bq(
		bq_client=bq_client,
		df=cur_df,
		table_id=endpoint_info['table_id'],
		mode='t' if trunc_flag else 'a',
		schema=endpoint_info['schema'],
		autodetect=True
	)


# main process
def main():
	# generate access token
	access_token = gen_access_token(TOKEN_URL, CLIENT_ID, CLIENT_SECRET, API_BASE_URL)
	
	for endpoint, endpoint_info in isams_dataset_endpoints.items():
		# construct full API path
		full_api_path = f"{API_BASE_URL}/{endpoint_info['url']}"

		# selectively run endpoints:
		if endpoint not in []:
			continue

		print(Fore.BLUE + f'{datetime.now()} Current endpoint:', endpoint)

		try:
			trunc_flag = True
			if endpoint_info['pages'] == 'multi-page':
				multi_page_endpoint(access_token, full_api_path, endpoint, endpoint_info, trunc_flag)
			else:
				single_page_endpoint(access_token, full_api_path, endpoint, endpoint_info, trunc_flag)
		except Exception as error:
			print(Fore.RED + f"Error processing endpoint '{full_api_path}'\n\n{error}")
			raise

		print(Fore.GREEN + f'{datetime.now()} Endpoint: {endpoint} loaded successfully')

if __name__ == '__main__':
	main()
	custom_pipelines()
