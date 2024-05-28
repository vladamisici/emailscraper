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
    # response = requests.get(
    #     'https://www.googleapis.com/gmail/v1/users/me/messages',
    #     headers={'Authorization': f'Bearer {credentials["token"]}'}
    # )
    # print(session.get('credentials'))
    if not session.get('credentials'):
        # return redirect(url_for('login.login_oauth'))
        return redirect('https://127.0.0.1:5000/authentication/login_oauth')

    try:
        # Load credentials from session
        credentials_json = session.get('credentials')
        # credentials_info = json.loads(credentials_json)

        # Create credentials object directly
        # creds = Credentials.from_authorized_user_info(credentials_info, SCOPES)
        creds=Credentials(**credentials_json)

        # Refresh credentials if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Call Gmail API with the credentials object
        service = build("gmail", "v1", credentials=creds)

        results = service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()    
        emails = results.get("messages", [])

        # Logic to determine the response based on email fetching
        if not emails:  # No emails found
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
    # # emails = [
    # #     {"id": 1, "subject": "Hello", "body": "Test email 1"},
    # #     {"id": 2, "subject": "Hi there", "body": "Test email 2"}
    # # ]
    # # return jsonify(emails)
    
@emails_bp.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('home'))
