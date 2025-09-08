import os
import calendar
from datetime import date, datetime, timedelta

'''
Files and folders
'''
# list all file names in a directory
# option to specify file type and full path or just file name
def file_type_in_dir(file_dir:str, file_ext:str, full_path=False):
	# parse checking
	if file_dir is None:
		file_dir = os.getcwd()
	elif not os.path.isdir(file_dir):
		raise ValueError(f'{file_dir} is not a directory')

	# file extension check
	if file_ext and not file_ext.startswith('.'):
		raise ValueError('Incorrect file extension')
	
	try:
		files_in_dir = os.listdir()
	except Exception as error:
		print(f'Could not list the files in directory. {file_dir} might not be an existing directory or user has no access to the dir\n{error}')
		raise

	# return all files or files with specific extension
	# return just file name or full file path
	if file_ext:
		return [(file if not full_path else f'{file_dir}/{file}') for file in files_in_dir]
	return ((file if not full_path else f'{file_dir}/{file}') for file in files_in_dir if file.endswith(file_ext))

# generate a filename with added prefix and suffix, along with specified file type
def gen_file_name(prefix:str, infile_name:str, infile_type:str, outfile_type:str, suffix:str):
	file_name = infile_name.replace(infile_type, '')
	final_file_name = f"{prefix}{file_name}{suffix}{outfile_type}"
	return final_file_name

# check if a file is plain text file (utf-8 encoding)
def is_plain_text_file(file_path:str):
	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			file.read()
		return True
	except UnicodeDecodeError:
		return False

'''
Datetime utils
'''
# get the current year
def get_month(in_date:date, name=False):
	if name:
		return in_date.strftime('%B')
	return in_date.month

def get_year(in_date:date):
	return in_date.year

def get_iso_weekyear(in_date:date=None, lpad:bool=False, lpad_num:int=0, backtrack:int=0):
	if not in_date:
		in_date = date.today()

	# backtrack n weeks from input date
	target_date = in_date - timedelta(week=backtrack)
	iso_week, iso_year, _ = target_date.iso_calendar()

	if lpad:
		if lpad_num >= 0:
			iso_week_str = str(iso_week).zfill(lpad)
			return iso_week_str
		else:
			raise ValueError('lpad must be an integer greater than 0')

	return (iso_week, iso_year)

'''
String formatting
'''
def snake_case(col: str) -> str:
	return col.lower().strip().replace(' ', '_').replace('-', '_')
