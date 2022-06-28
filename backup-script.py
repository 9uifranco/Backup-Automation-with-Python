# core python

import os
import os.path

# google stuffs

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


# ------  AUTHORIZATION & AUTHENTICATION ------ #

# scopes basically says what we gonna do with the script
# we r going to use /drive to use google drive, but if more scopes are needed just look at the google documentation
# if you add more scopes, you gonna need refresh the token (delete it & create a new one)


SCOPES = ['https://wwww.googleapis.com/auth/drive'] 

creds = None

# here we r loading the credentials when we already authorized'em, when we have the token already

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)   

# if we don't have the token or if it's expired or invalid for some reason

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request()) # if the creds are there, but they are expired, we will refresh them
    else: # if we don't have the credentials
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES) #create the AppFlow from the credentials file
        creds = flow.run_local_server(port=0)

    with open('token.json', 'w') as token: # create the token file with writing mode
        token.write(creds.to_json()) # taking that object and putting into a json file

# ------- BACKING UP FILES -------- #

try:
    # create a service and try to access the google drive api with our authorization
    service = build("drive", "v3", credentials=creds)
    # do the request and get the response
    response = service.files().list(
        q="name='BackupFolder' and mimeType='application/vnd.google-apps.folder'",
        spaces='drive'
    ).execute()
    # if there's no folder, we r going to create a new one
    if not response['files']:
        # metadata
        file_metadata = {
            "name": "BackupFolder",
            "mimeType": "application/vnd.google-apps.folder"
        }
        # create the file
        file = service.files().create(body=file_metadata, fields="id").execute()
        # get the folder id to put stuff in it
        folder_id = file.get('id')
    # if the folder exist
    else:
        folder_id = response['files'][0]['id']
    # iterate through the files we have in the local bakcup folder and upload to the remote folder
    for file in os.listdir('backup-1'): # list all the files in the directory
        file_metadata = {
            "name": file,
            "parents": [folder_id] 
        }

        media = MediaFileUpload(f"backup-1/{file}")
        upload_file = service.files().create(body=file_metadata,
                                            media_body=media,
                                            fields="id").execute()
        
        print("Backed up file: " + file)

except HttpError as e:
    print("Error: " + str(e))