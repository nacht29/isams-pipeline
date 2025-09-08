import os
import calendar
from typing import Optional, List
from google.cloud import bigquery as bq
from file_format import content_data

OS = os.name

'''
File data to BQ (Excel/CSV)
'''

def file_to_bucket(bucket_client, bucket_id:str, bucket_filepath:str, file_type:str, file_path:str, mode:str, log=False) -> None:
	# parse error handling
	if mode not in ('i', 't'):
		raise ValueError("Incorrect write mode. Must be 'i' for ignore, or 't' for truncate")
	if file_type not in content_data:
		raise ValueError(f'Invalid file type. Supported: {list(content_data.keys())}')
	
	# file integrity
	if not os.path.exists(file_path):
		raise ValueError(f'{file_path} not found')
	if not os.path.isfile(file_path):
		raise ValueError(f'{file_path} is not a file')

	# constructing full file path in bucket based on file name and base bucket path
	# os.path.basename extracts the file name from the full file path
	file_name = os.path.basename(file_path)
	full_path = f'{bucket_filepath}/{file_name}' if bucket_filepath else file_name

	# upload process
	try:
		# create file blob for upload - blob is a binary representation of the file to be uploaded
		blob = bucket_client.bucket(bucket_id).blob(full_path)

		# skip upload if in ignore mode and file exists
		if mode == 'i' and blob.exists():
			print(f'Skipping file {full_path} as it already exists.') if log else 0
			return

		# upload blob
		blob.upload_from_filename(file_path, content_type=content_data[file_type]['content_type'])
		print(f"Uploaded {content_data[file_type]['type_name']} {file_path} to {bucket_filepath if bucket_filepath else '/'}") if log else 0
	except Exception:
		print(f"Failed to upload {content_data[file_type]['type_name']} {file_path} to {bucket_filepath if bucket_filepath else '/'}") if log else 0
		raise

def bucket_csv_to_bq(bq_client, bucket_filepath:str, project_id:str, dataset_id:str, table_id:str, write_mode:str, skip_leading_rows:int=1, schema:Optional[List[bq.SchemaField]]=None, log:bool=False) -> None:
	if write_mode not in ('a', 't'):
		raise ValueError("Incorrect write mode. Must be 'a' for append or 't' for truncate.")
	if bucket_filepath.startswith('gs://'):
		raise ValueError("Do not inclide 'gs://' in bucket file path.")
	
	job_config = bq.LoadJobConfig(
		source_format=bq.SourceFormat.CSV,
		skip_leading_rows=skip_leading_rows,
		write_disposition='WRITE_TRUNCATE' if write_mode == 't' else 'WRITE_APPEND',
		autodetect=not schema, # if schema == True, not schema = False and vice versa - set to True if schema is not provided and vice versa
		schema=schema
	)

	uri = f'gs://{bucket_filepath}'

	try:
		job = bq_client.load_table_from_uri(
			uri,
			destination=f'{project_id}.{dataset_id}.{table_id}',
			job_config=job_config
		)
		print(f'Successfully loaded {bucket_filepath} to {project_id}.{dataset_id}.{table_id}')
		job.result()
	except Exception as error:
		print(f'Failed to load {bucket_filepath} to {project_id}.{dataset_id}.{table_id}. Error: {error}') if log else ''
		raise

def bucket_excel_to_bq(bq_client, bucket_filepath:str, project_id:str, dataset_id:str, table_id:str, write_mode:str, schema:Optional[List[bq.SchemaField]]=None, log:bool=False) -> None:
	if write_mode not in ('a', 't'):
		raise ValueError("Incorrect write mode. Must be 'a' for append or 't' for truncate.")
	if bucket_filepath.startswith('gs://'):
		raise ValueError("Do not inclide 'gs://' in bucket file path.")
	
	job_config = bq.LoadJobConfig(
		source_format=bq.SourceFormat.XLSX,
		write_disposition='WRITE_TRUNCATE' if write_mode == 't' else 'WRITE_APPEND',
		autodetect=not schema,
		schema=schema
	)

	uri = f'gs://{bucket_filepath}'

	try:
		job = bq_client.load_table_from_uri(
			uri,
			destination=f'{project_id}.{dataset_id}.{table_id}',
			job_config=job_config
		)
		print(f'Successfully loaded {bucket_filepath} to {project_id}.{dataset_id}.{table_id}')
		job.result()
	except Exception as error:
		print(f'Failed to load {bucket_filepath} to {project_id}.{dataset_id}.{table_id}. Error: {error}') if log else ''
		raise

'''
Expansion:
- ETL from various databases to data warehouse
'''