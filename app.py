import streamlit as st
from datetime import datetime, time
import pytz
import os
import json
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pickle


# Streamlit Secrets Configuration
def get_google_creds():
    if st.secrets.get("google"):  # Production (Streamlit Sharing)
        return {
            "installed": {
                "client_id": st.secrets.google.client_id,
                "project_id": st.secrets.google.project_id,
                "auth_uri": st.secrets.google.auth_uri,
                "token_uri": st.secrets.google.token_uri,
                "client_secret": st.secrets.google.client_secret,
                "redirect_uris": [st.secrets.google.redirect_uri]
            }
        }
    else:  # Local development
        with open('credentials.json') as f:
            return json.load(f)


def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                get_google_creds(),
                ['https://www.googleapis.com/auth/calendar']
            )
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

# Rest of your Streamlit app code (same as previous version)
# [Include all the previous Streamlit UI and logic here]