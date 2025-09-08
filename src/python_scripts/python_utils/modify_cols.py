import pandas as pd

TIMEZONE = 'Asia/Singapore'

def parse_datetime_utc8(date_col:pd.Series) -> pd.Series:
	date_col = pd.to_datetime(date_col, utc=True, errors="coerce")
	return date_col.dt.tz_convert(TIMEZONE)

def applicants_mod(applicants_df:pd.DataFrame):
	date_cols = ['dateOfBirth', 'enquiryDate', 'enrolmentDate', 'lastUpdated', 'registeredDate', 'withdrawnDate']
	
	for date_col in date_cols:
		applicants_df[date_col] = parse_datetime_utc8(applicants_df[date_col])

	return applicants_df

def school_terms_mod(terms_df:pd.DataFrame):
	date_cols = ['finishDate', 'startDate']

	for date_col in date_cols:
		terms_df[date_col] = parse_datetime_utc8(terms_df[date_col])

	return terms_df

def students_mod(students_df:pd.DataFrame):
	date_cols = ['dob', 'enrolmentDate', 'lastUpdated', 'leavingDate']

	for date_col in date_cols:
		students_df[date_col] = parse_datetime_utc8(students_df[date_col])
	return students_df

def alumni_mod(alumni_df:pd.DataFrame):
	date_cols = ['lastUpdated']

	for date_col in date_cols:
		alumni_df[date_col] = parse_datetime_utc8(alumni_df[date_col])

	return alumni_df

def year_group_mod(year_grp_df:pd.DataFrame):
	year_grp_df['lastUpdated'] = parse_datetime_utc8(year_grp_df['lastUpdated'])
	return year_grp_df

def billing_cycles_mod(billing_df:pd.DataFrame):
	date_cols = ['earlyPaymentDate', 'startDate']

	for date_col in date_cols:	
		billing_df[date_col] = parse_datetime_utc8(billing_df[date_col])
	
	billing_df['endDate'] = None
	
	return billing_df
