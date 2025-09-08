import pandas as pd
from io import BytesIO
from datetime import datetime
from google.cloud import bigquery as bq

def df_to_bq(bq_client, df:pd.DataFrame, table_id:str, mode:str, schema=None, autodetect:bool=True):
	if mode == 'a':
		write_disposition = 'WRITE_APPEND'
	elif mode == 't':
		write_disposition ="WRITE_TRUNCATE"
	else:
		raise ValueError(f"{mode} is not recognised. Use 'a' for append or 't' for truncate")

	try:
		job_config = bq.LoadJobConfig(schema=schema, write_disposition=write_disposition, autodetect=autodetect)
		job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
		job.result()
		return job
	except Exception:
		raise
