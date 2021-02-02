import os
import pickle
import sys

from google.auth.transport import requests
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from requests import RequestException

from models import CLIENT_SECRET_FILE, API_VERSION, API_NAME, SCOPES, shared_folder_id
from models.os_functions import remove_unnecessary_files


# -----------------------------------------------------------------------------------------------------
def create_service(client_secret_file, api_name, api_version, *scopes):
    print(os.getcwd())
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


# -----------------------------------------------------------------------------------------------------
def upload_files_to_drive(files_to_upload):
    try:
        service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        for file_name in files_to_upload:
            file_metadata = {
                'name': file_name,
                'parents': [shared_folder_id],
            }
            'storage/{0}'.format(file_name)
            media = MediaFileUpload('storage/{0}'.format(file_name))
            r = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            if len(r.get('id')) > 0:
                print("workbook: " + file_name + " was uploaded to drive")
            else:
                raise RequestException("The workbook was not uploaded to google drive")

    except requests.exceptions as e:
        print(e)
        print("there was an issue with google api - upload file function")
        print('delete content from storage')
        remove_unnecessary_files('storage')
        print("program ends")
        sys.exit()

# -----------------------------------------------------------------------------------------------------
