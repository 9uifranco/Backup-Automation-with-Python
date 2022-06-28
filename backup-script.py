# core python

import os
import os.auth

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


SCOPES = ["https://wwww.googleapis.com/auth/drive"] 

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



