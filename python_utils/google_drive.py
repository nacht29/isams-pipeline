import os
import openpyxl
from io import BytesIO
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload
from python_utils.formats import content_data
from python_utils.utils import *

'''
Credentials
'''

# build and return Google Drive service client
def build_drive_service(service_account_key) -> Resource:
	scopes = ["https://www.googleapis.com/auth/drive"]
	creds = service_account.Credentials.from_service_account_file(service_account_key, scopes=scopes)
	service = build('drive', 'v3', credentials=creds)
	return service

class Google_Drive:
	def __init__(self, service, is_shared_drive:str, main_drive_id:str):
		if not isinstance(is_shared_drive, bool):
			raise ValueError('is_shared_drive must be type <bool>')
		
		self.service = service
		self.is_shared_drive = is_shared_drive
		if not is_shared_drive:
			if main_drive_id == 'my-drive':
				self.main_drive_id = 'root'
			else:
				raise ValueError('Invalid parent folder Id') 
		else:
			self.main_drive_id = main_drive_id

	'''
	Helper functions
	'''
	# returns a list of duplicate file id and names
	def drive_get_dup_files(self, dst_folder_id:str, file_name:str, log:bool=False) -> list:
		query = f"""
		'{dst_folder_id}' in parents
		and name='{file_name}'
		and trashed=false
		"""

		try:
			results = self.service.files().list(
					q=query,
					fields='files(id, name)',
					supportsAllDrives=self.is_shared_drive,
					includeItemsFromAllDrives=self.is_shared_drive
			).execute()
		except Exception as error:
			if log:
				print(f'Unable to read folder Id {dst_folder_id}\n{error}')
			raise

		# get dup file id
		dup_files = results.get('files', [])

		return dup_files

	# create/upload a new file in Google Drive
	# allow duplicates
	def drive_create_file(self, file_metadata:dict, media, log:bool=False):
		if log:
			print(f"{datetime.now()} Creating {file_metadata['name']}")
		try:
			self.service.files().create(
				body=file_metadata,
				media_body=media,
				fields='id',
				supportsAllDrives=self.is_shared_drive
			).execute()
		except Exception as error:
			if log:
				print(f"Error processing: {file_metadata['name']}\n{error}")
			raise

	# update file in Drive if the file being uploaded alr exists
	# truncate duplicate files
	def drive_update_file(self, media, dup_files:list, log:bool=False):
		if log:
			print(f"{datetime.now()} Updating {dup_files[0]['name']}")

		dup_file_id = dup_files[0]['id']
		try:
			self.service.files().update(
				fileId=dup_file_id,
				media_body=media,
				supportsAllDrives=self.is_shared_drive
			).execute()
		except Exception as error:
			if log:
				print(f"Error processing: {dup_files[0]['name']}\n{error}")
			raise

	'''
	Search/Autodetect
	'''
	# look for folder by folder name - user can choose to create folder if it does not exist yet
	# parent_folder_id = folder id before the target folder
	# return (folder_id, folder_name and last_modified)
	def drive_autodetect_folders(self, parent_folder_id:str, folder_name:str, create_folder:bool, log:bool=False) -> list:
		query = f"""
		'{parent_folder_id}' in parents
		and name='{folder_name}'
		and mimeType='application/vnd.google-apps.folder' 
		and trashed=false
		"""

		try:
			# execute the query
			results = self.service.files().list(
				q=query,
				fields='files(id, name, modifiedTime)',
				orderBy='modifiedTime desc',
				pageSize=1,
				supportsAllDrives=self.is_shared_drive,
				includeItemsFromAllDrives=self.is_shared_drive
			).execute()
		except Exception as error:
			if log:
				print(f"Unable to autodetect '{folder_name}' in folder Id '{parent_folder_id}\n{error}'")
			raise

		folders_in_drive = results.get('files', []) # files_in_drive = results.get('files', [])

		if folders_in_drive:
			return folders_in_drive[0]
		elif not folders_in_drive and create_folder:
			folder_metadata = {
				'name': folder_name,
				'mimeType': 'application/vnd.google-apps.folder',
				'parents': [parent_folder_id]
			}

			try:
				folder = self.service.files().create(
					body=folder_metadata,
					fields='id, name',
					supportsAllDrives=self.is_shared_drive
					# note that for .create, there is no need to includeItemsFromAllDrives=is_shared_drive
				).execute()
			except Exception as error:
				if log:
					print(f"Unable to create '{folder_name}' in folder Id '{parent_folder_id}'")
				raise

			return folder

		return []

	# search a file by name in Google Drive
	# return (file_id, file_name, last_modified)
	def drive_search_filename(self, parent_folder_id: str, file_name:str) -> list:
		query = f"""
		'{parent_folder_id}' in parents
		and name = '{file_name}'
		and trashed=false
		"""
		
		try:
			response = self.service.files().list(
				q=query,
				fields='files(id, name, modifiedTime)',
				orderBy='modifiedTime desc',
				pageSize=1,
				supportsAllDrives=self.is_shared_drive,
				includeItemsFromAllDrives=self.is_shared_drive,
			).execute()
			
			files = response.get('files', [])
			if files:
				return files[0]
			else:
				return []
				
		except Exception as error:
			return []

	'''
	Upload files
	'''

	# uploads a locally stored file to Google Drive
	def local_file_to_drive(self, dst_folder_id:str, file_path:str, update_dup=True, log=False):
		# parse error handling
		if not isinstance(update_dup, bool):
			raise ValueError('Update dup must be value type <bool>')
		
		# file integrity
		file_name = os.path.basename(file_path)
		file_ext = os.path.splitext(file_name)[1]

		if file_ext not in content_data:
			raise ValueError(f'Invalid file type. Supported: {list(content_data.keys())}')	
		if not os.path.isfile(file_path):
			raise ValueError(f'{file_path} is not a file')
		
		# file metadata
		file_metadata = {
			'name': file_name,
			'parents': [dst_folder_id],
			'driveId': self.main_drive_id
		}

		# determine mimetype and read mode
		mime_type = content_data[file_ext]['content_type']
		mode = 'r' if is_plain_text_file(file_path) else 'rb'

		# upload process
		try:
			with open(file_path, mode) as file:
				media = MediaIoBaseUpload(
					file,
					mimetype=mime_type,
					resumable=True
				)

				if update_dup:
					dup_files = self.drive_get_dup_files(dst_folder_id, file_name, log)

					# update existing files or create new ones
					if dup_files:
						self.drive_update_file(media, dup_files, log)
					else:
						self.drive_create_file(file_metadata, media, log)

				else:
					self.drive_create_file(file_metadata, media, log)
		except Exception as error:
			print(f'Upload failed for {file_path}\n{error}') if log else 0
			raise

	# uploads a binary file data to Google Drive
	# file data taken in the form of tuple: (file name, file buffer, file type)
	def bin_file_to_drive(self, dst_folder_id:str, file_data:tuple, update_dup=True, log=False):
		# parsing check
		if update_dup not in (True, False):
			raise ValueError('Update dup must be value type <bool>')
		if not isinstance(file_data, tuple) or len(file_data) != 3:
			raise ValueError('file data must be a tuple of len = 3, in the form of (file name, file buffer, file type)')
		if file_data[2] not in content_data:
			raise ValueError(f'Invalid file type. Supported: {list(content_data.keys())}')

		# file metadata prep
		file_metadata = {
			'name': file_data[0],
			'parents': [dst_folder_id],
			'driveId': self.main_drive_id
		}

		# try to move pointer to first byte in file buffer
		file_buffer = file_data[1]
		if hasattr(file_buffer, 'seek'):
			file_buffer.seek(0)
		else:
			raise ValueError('Incorrect tuple')

		# MediaBaseUpload media object
		media = MediaIoBaseUpload(
			file_data[1], # file buffer
			mimetype=content_data[file_data[2]]['content_type'],
			resumable=True
		)

		# upload process
		try:
			if update_dup:
				dup_files = self.drive_get_dup_files(dst_folder_id, file_data[0], log)

				# update existing files or create new ones
				if dup_files:
					self.drive_update_file(media, dup_files, log)
				else:
					self.drive_create_file(file_metadata, media, log)
			else:
				self.drive_create_file(file_metadata, media, log)
		except Exception as error:
			print(f'Upload failed for {file_metadata['name']}\n{error}') if log else 0
			raise

	'''
	Read/download files
	'''

	def download_file_from_drive(self, dst_folder_id:str):
		pass

	def read_excel_to_df(self, dst_folder_id:str, file_metadata:tuple, log=False):
		pass