from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import jsonify, Blueprint, session, redirect, url_for
from dotenv import load_dotenv
import os
import json
load_dotenv()
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')

emails_bp = Blueprint('emails', __name__)

@emails_bp.route("/inbox")
def get_inbox():
    credentials_json = session.get('credentials')

    Credentials_info = json.loads(credentials_json)

    if credentials_json:
        creds = Credentials.from_authorized_user_info(Credentials_info, SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        session['credentials'] = creds.to_json()

        try:
            # Call the Gmail API
            service = build("gmail", "v1", credentials=creds)
            results = service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()    
            emails = results.get("messages", [])

            if not emails:
                return "No emails", 200
    
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
            return f'Error: {str(error)}', 500
    else:
        return 'Unauthorized', 401
    
@emails_bp.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('home'))
