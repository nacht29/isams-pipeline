import requests
from typing import Any

def gen_access_token(token_url:str, client_id:str, client_secret:str, api_base_url:str):
	try:
		token_request = requests.post(
			token_url,
			data={
				'grant_type': 'client_credentials',
				'client_id': client_id,
				'client_secret': client_secret
			}
		)
	except Exception as error:
		print(f"Unable to request access token for '{api_base_url}' with client_id '{client_id}'\n{error}")

	access_token = token_request.json()['access_token']
	return access_token

def api_get(access_token:str, api_url:str, content_type:str=None, params:dict=None):
	headers = {
		'Authorization': f'Bearer {access_token}'
	}

	if content_type:
		headers['Content-Type'] = content_type

	try:
		if params:
			api_response = requests.get(api_url, headers=headers, params=params)
		else:
			api_response = requests.get(api_url, headers=headers, params=params)
	except Exception as error:
		print(f"Failed to reach '{api_url}'\n{error}")
	return (api_response.json())

'''
def is_nested_field(field_value:Any):
	status = False

	if isinstance(field_value, list) and all(isinstance(item, dict) for item in field_value):
		status = True
	if isinstance(field_value, dict):
		status = True

	return status
'''