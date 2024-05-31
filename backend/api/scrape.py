from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import jsonify, Blueprint, session, redirect, url_for
from dotenv import load_dotenv
import requests
import os
import json
from flask_cors import CORS
load_dotenv()
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')

emails_bp = Blueprint('emails', __name__)
CORS(emails_bp, resources={r"*": {"origins": "https://localhost:5173", "supports_credentials": True}})

@emails_bp.route("/inbox")
def get_inbox():
    if not session.get('credentials'):
        # return redirect(url_for('login.login_oauth'))
        return redirect('https://127.0.0.1:5000/authentication/login_oauth')

    try:
        credentials_json = session.get('credentials')
        # credentials_info = json.loads(credentials_json)

        creds=Credentials(**credentials_json)

        # Refresh credentials if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Call Gmail API with the credentials object
        service = build("gmail", "v1", credentials=creds)

        results = service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()    
        emails = results.get("messages", [])

        if not emails:
            return jsonify({"message":"no emails"}), 200
        inbox_content = []
        for email in emails:
            msg = service.users().messages().get(userId="me", id=email["id"]).execute()
            subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
            snippet = msg.get('snippet', '')
            sender = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), None)
            timestamp = msg.get('internalDate', '')
            inbox_content.append({'subject': subject, 'snippet': snippet, 'from': sender, 'time': timestamp})
        return jsonify(inbox_content), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@emails_bp.route("/sent")
def get_sent_emails():
    if not session.get('credentials'):
        return redirect('https://127.0.0.1:5000/authentication/login_oauth')

    try:
        credentials_json = session.get('credentials')
        creds = Credentials(**credentials_json)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        service = build("gmail", "v1", credentials=creds)

        results = service.users().messages().list(userId="me", labelIds=["SENT"]).execute()    
        emails = results.get("messages", [])

        if not emails:
            return jsonify({"message":"no sent emails"}), 200

        sent_content = []
        for email in emails:
            msg = service.users().messages().get(userId="me", id=email["id"]).execute()
            subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
            snippet = msg.get('snippet', '')
            receiver = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'To'), None)
            timestamp = msg.get('internalDate', '')
            sent_content.append({'subject': subject, 'snippet': snippet, 'to': receiver, 'time': timestamp})
        return jsonify(sent_content), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@emails_bp.route("/drafts")
def get_draft_emails():
    if not session.get('credentials'):
        return redirect('https://127.0.0.1:5000/authentication/login_oauth')

    try:
        credentials_json = session.get('credentials')
        creds = Credentials(**credentials_json)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        service = build("gmail", "v1", credentials=creds)

        results = service.users().drafts().list(userId="me").execute()    
        drafts = results.get("drafts", [])

        if not drafts:
            return jsonify({"message":"no draft emails"}), 200

        draft_content = []
        for draft in drafts:
            draft_msg = service.users().drafts().get(userId="me", id=draft["id"]).execute()
            msg = draft_msg['message']
            subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
            snippet = msg.get('snippet', '')
            receiver = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'To'), None)
            timestamp = msg.get('internalDate', '')
            draft_content.append({'subject': subject, 'snippet': snippet, 'to': receiver, 'time': timestamp})
        return jsonify(draft_content), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500


# @emails_bp.route("/inbox")
# def get_inbox():
#     global last_history_id

#     if not session.get('credentials'):
#         return redirect('https://127.0.0.1:5000/authentication/login_oauth')

#     try:
#         credentials_json = session.get('credentials')
#         creds = Credentials(**credentials_json)

#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())

#         service = build("gmail", "v1", credentials=creds)
#         inbox_label = service.users().labels().get(userId="me", id="INBOX").execute()

#         start_history_id = last_history_id if last_history_id else '1' 
#         history = service.users().history().list(userId="me", startHistoryId=start_history_id).execute()
#         history_records = history.get('history', [])

#         inbox_content = []

#         for record in history_records:
#             for message_change in record.get('messages', []):
#                 # Fetch the details of the new or updated message
#                 msg = service.users().messages().get(userId="me", id=message_change['id']).execute()
#                 subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
#                 snippet = msg.get('snippet', '')
#                 sender = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), None)
#                 timestamp = msg.get('internalDate', '')

#                 # Append email details to inbox_content list
#                 inbox_content.append({'subject': subject, 'snippet': snippet, 'from': sender, 'time': timestamp})

#         # Update last_history_id with the most recent historyId
#         if history_records:
#             last_history_id = history_records[-1]['id']

#         # Return the inbox_content as JSON response
#         return jsonify(inbox_content), 200

#     except Exception as error:
#         return jsonify({"error": str(error)}), 500
    
emails_bp.route('/logout')
def logout():
    session.clear()
    return redirect('https://localhost:5173')
