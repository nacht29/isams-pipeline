def csv_to_bucket(bucket_client, bucket_id:str, bucket_filepath:str, csv_file_path:str, mode:str, log=False) -> None:
	if mode not in ('i', 't'):
		raise ValueError("Incorrect write mode. Must be 'i' for ignore, or 't' for truncate.")

	try:
		bucket = bucket_client.get_bucket(bucket_id)
	except Exception:
		if log:
			print(f'Failed to access {bucket_id}')
		raise

	try:
		# identify csv file name from local file path
		if OS == 'posix':
			csv_filename = csv_file_path.split('/')[-1]
		elif OS == 'nt':
			csv_filename = csv_file_path.split('\\')[-1]
		else:
			raise OSError('Unidentified OS. Allowed: Windows, Linux, Darwin.')

		# set dst for csv file in bucket
		full_path = f'{bucket_filepath}/{csv_filename}' if bucket_filepath else csv_filename
	except Exception:
		print(f'Failed to load CSV to {bucket_id}') if log else ''
		raise

	try:
		# look for exisiting duplicates
		# create file blob for upload - blob is a binary representation of the file to be uploaded
		blob = bucket_client.bucket(bucket_id).blob(full_path)
		if not (mode == 'i' and blob.exists()):
			blob.upload_from_filename(csv_file_path, content_type="text/csv")
			print(f"Uploaded {csv_file_path} to {bucket_filepath if bucket_filepath else '/'}") if log else ''
	except Exception:
		print(f"Failed to upload {csv_file_path} to {bucket_filepath if bucket_filepath else '/'}") if log else ''
		raise

def excel_to_bucket(bucket_client, bucket_id:str, bucket_filepath:str, excel_file_path:str, mode:str, log=False) -> None:
	if mode not in ('i', 't'):
		raise ValueError("Incorrect write mode. Must be 'i' for ignore, or 't' for truncate.")

	try:
		bucket = bucket_client.get_bucket(bucket_id)
	except Exception:
		if log:
			print(f'Failed to access {bucket_id}')
		raise

	try:
		# identify Excel file name from local file path
		if OS == 'posix':
			excel_filename = excel_file_path.split('/')[-1]
		elif OS == 'nt':
			excel_filename = excel_file_path.split('\\')[-1]
		else:
			raise OSError('Unidentified OS. Allowed: Windows, Linux, Darwin.')

		# set dst for Excel file in bucket
		full_path = f'{bucket_filepath}/{excel_filename}' if bucket_filepath else excel_filename
	except Exception:
		print(f'Failed to load Excel to {bucket_id}') if log else ''
		raise

	try:
		# look for exisiting duplicates
		# create file blob for upload - blob is a binary representation of the file to be uploaded
		blob = bucket_client.bucket(bucket_id).blob(full_path)
		if not (mode == 'i' and blob.exists()):
			blob.upload_from_filename(excel_file_path, content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
			print(f"Uploaded {excel_file_path} to {bucket_filepath if bucket_filepath else '/'}") if log else ''
	except Exception:
		print(f"Failed to upload {excel_file_path} to {bucket_filepath if bucket_filepath else '/'}") if log else ''
		raise
