from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import jsonify, Blueprint, session, redirect, url_for, request
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
    if not session.get('credentials'):
        return redirect(url_for('login.login_oauth'))

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
        return f'Error: {str(error)}', 500


@emails_bp.route('/sent')
def get_sent():
    credentials_json = session.get('credentials')
    Credentials_info = json.loads(credentials_json)

    if credentials_json:
        creds = Credentials.from_authorized_user_info(Credentials_info, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        session['credentials'] = creds.to_json()

        try:
            service = build("gmail", "v1", credentials=creds)
            results = service.users().messages.list(userId='me', labelIds=["SENT"]).execute()
            sent_mails = results.get("messages", [])

            if not sent_mails:
                return "No sent emails"
            
            sent_content = []

            for email in sent_mails:
                msg = service.users().messages().get(userId="me", id=email["id"]).execute()
                subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
                snippet = msg.get('snippet', '')
                
                # Extract recipients from 'To', 'Cc', or 'Bcc' fields in the headers
                to_recipients = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'To']
                cc_recipients = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'Cc']
                bcc_recipients = [header['value'] for header in msg['payload']['headers'] if header['name'] == 'Bcc']
                
                all_recipients = ', '.join(to_recipients + cc_recipients + bcc_recipients)
                
                timestamp = msg.get('internalDate', '')
                sent_content.append({'subject': subject, 'snippet': snippet, 'recipients': all_recipients, 'time': timestamp})
            return jsonify(sent_content), 200
        except Exception as error:
            return f'Error: {str(error)}', 500
    else:
            return 'Unauthorized', 401

@emails_bp.route("/validate_token", methods=['POST'])
def validate_token():
    # Extract access token from request (consider using a secure method like headers)
    access_token = request.json.get('access_token')
    if not access_token:
        return 'Missing access token', 401

    try:
        # Use a library like google-auth-oauthlib to validate the token

        credentials = Credentials.from_authorized_user_info({
            'access_token': access_token
        }, SCOPES)

        # Optional: Check token expiration and refresh if needed
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        # Token is valid, use credentials to access Gmail API
        service = build("gmail", "v1", credentials=credentials)
        # ... perform Gmail API calls with the validated service object ...

    except Exception as error:
        return f'Invalid token or error: {str(error)}', 401

    return 'Token valid', 200

@emails_bp.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('home'))
