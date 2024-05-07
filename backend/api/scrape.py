from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, jsonify, Blueprint, session
from dotenv import load_dotenv
import os
import json
load_dotenv()
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://mail.google.com/"]
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')

emails_bp = Blueprint('emails', __name__, url_prefix='/emails')

@emails_bp.route("/emails")
def get_emails():
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
                inbox_content.append({'subject': subject, 'snippet': snippet})
            return jsonify(inbox_content), 200
    
        except Exception as error:
            return f'Error: {str(error)}', 500
    else:
        return 'Unauthorized', 401
























# import imaplib
# import email
# import yaml
# import jsonify

# from flask import Blueprint

# with open("credentials.yaml") as f:
#     content = f.read()

# credentials = yaml.load(content, Loader=yaml.FullLoader)

# user, password = credentials['user'], credentials['password']






# def fetch_emails(user, password):
#     imap_url = "imap.gmail.com"
#     my_mail = imaplib.IMAP4_SSL(imap_url)
#     my_mail.login(user,password)
#     my_mail.select("INBOX")
#     _, data = my_mail.search(None, 'ALL')
#     id_list = data[0].split()
#     messages = []

#     for msg in id_list:
#         typ, data = my_mail.fetch(msg, '(RFC822)')
#         messages.append(data)

#     emails = []

#     for msg in messages[::-1]:
#         for response in msg:
#             if isinstance(response, tuple):
#                 my_msg = email.message_from_bytes((response[1]))
#                 email_data = {
#                     'subject': my_msg['subject'],
#                     'from': my_msg['from'],
#                     'body': ''
#                 }
#                 for part in my_msg.walk():
#                     if part.get_content_type() == 'text/plain':
#                         email_data['body'] = part.get_payload()
#                 emails.append(email_data)
#     return emails

