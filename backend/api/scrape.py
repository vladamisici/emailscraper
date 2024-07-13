from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import jsonify, Blueprint, session, redirect, url_for, request
from dotenv import load_dotenv
import requests
import os
import json
from flask_cors import CORS, cross_origin
import flask
from email.message import EmailMessage
import base64
from datetime import datetime
from email.utils import formatdate
import concurrent.futures
from collections import Counter

load_dotenv()
SCOPES = ["https://mail.google.com/"]
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')

emails_bp = Blueprint('emails', __name__)
CORS(emails_bp, supports_credentials=True, resources={r"*": {"origins": "https://localhost:5173"}})

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

            payload = msg['payload']
            body = ''
            if payload.get('body', {}).get('data'):
                body = base64.urlsafe_b64decode(payload['body']['data'].encode('ASCII')).decode('utf-8')
            elif payload.get('parts'):
                for part in payload['parts']:
                    if part['mimeType'] == 'text/plain':
                        body = base64.urlsafe_b64decode(part['body']['data'].encode('ASCII')).decode('utf-8')

            if timestamp:
                timestamp = int(timestamp)//1000
                date_format = "%Y-%m-%d %H:%M"
                formatted_date = datetime.fromtimestamp(timestamp).strftime(date_format)
            else:
                formatted_date = '' 
            inbox_content.append({'subject': subject, 'snippet': snippet, 'from': sender, 'date': formatted_date, 'content': body})
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
            timestamp = msg.get('internalDate', '')
            if timestamp:
                timestamp = int(timestamp)//1000
                date_format = "%Y-%m-%d %H:%M"
                formatted_date = datetime.fromtimestamp(timestamp).strftime(date_format)
            else:
                formatted_date = '' 
            sent_content.append({'subject': subject, 'snippet': snippet, 'to': receiver, 'date': formatted_date})
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
            timestamp = msg.get('internalDate', '')
            if timestamp:
                timestamp = int(timestamp)//1000
                date_format = "%Y-%m-%d %H:%M"
                formatted_date = datetime.fromtimestamp(timestamp).strftime(date_format)
            else:
                formatted_date = '' 
            draft_content.append({'subject': subject, 'snippet': snippet, 'to': receiver, 'date': formatted_date})
        return jsonify(draft_content), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@emails_bp.route("/spam")
def get_spam():
    if not session.get('credentials'):
        return redirect('https://127.0.0.1:5000/authentication/login_oauth')

    try:
        credentials_json = session.get('credentials')
        creds = Credentials(**credentials_json)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        service = build("gmail", "v1", credentials=creds)

        results = service.users().messages().list(userId="me", labelIds=["SPAM"]).execute()
        emails = results.get("messages", [])

        if not emails:
            return jsonify({"message": "no spam emails"}), 200

        spam_content = []
        for email in emails:
            msg = service.users().messages().get(userId="me", id=email["id"]).execute()
            subject = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'Subject'), None)
            snippet = msg.get('snippet', '')
            sender = next((header['value'] for header in msg['payload']['headers'] if header['name'] == 'From'), None)
            timestamp = msg.get('internalDate', '')
            if timestamp:
                timestamp = int(timestamp) // 1000
                date_format = "%Y-%m-%d %H:%M"
                formatted_date = datetime.fromtimestamp(timestamp).strftime(date_format)
            else:
                formatted_date = ''
            spam_content.append({'subject': subject, 'snippet': snippet, 'from': sender, 'date': formatted_date})

        return jsonify(spam_content), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@emails_bp.route("/send_email", methods=["POST"])
@cross_origin(origins=["https://localhost:5173"], supports_credentials=True)
def send_email():
    data = request.json
    to_email = data.get('toEmail')
    subject = data.get('subject')
    message_content = data.get('messageContent')
    schedule_time = data.get('scheduleTime')
    sender_email = session.get('email')
    if not sender_email:
        return jsonify({'error': 'Sender email not found in session'}), 401
    
    try:
        credentials_json = session.get('credentials')
        creds = Credentials(**credentials_json)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()
        message.set_content(message_content)
        message["To"] = to_email
        message["Subject"] = subject
        message["From"] = sender_email

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {"raw": encoded_message}
        if schedule_time:
            scheduled_time_ms = int(datetime.fromisoformat(schedule_time).timestamp() * 1000)
            create_message["internalDate"] = scheduled_time_ms
        else:
            create_message = {"raw":encoded_message}
        sent_message = service.users().messages().send(userId="me", body=create_message).execute()

        return jsonify({'success': True, 'message_id': sent_message['id']}), 200
    except HttpError as error:
        return jsonify({'error': f"Error: {error}"}), 500

@emails_bp.route("/analysis")
@cross_origin(origins=["https://localhost:5173"], supports_credentials=True)
def get_email_analysis():
    response, status_code = get_inbox()
    
    if status_code != 200:
        return jsonify({"error": "Failed to fetch emails"}), status_code

    emails = response.json

    if not emails:
        return jsonify({
            'weekdayData': [0] * 7,
            'hourlyData': [0] * 24
        })

    def process_batch(batch):
        weekday_data = [0] * 7
        hourly_data = [0] * 24
        for email in batch:
            date_str = email.get('date')
            if date_str:
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                    weekday_data[date.weekday()] += 1
                    hourly_data[date.hour] += 1
                except ValueError:
                    print(f"Invalid date format: {date_str}")
        return weekday_data, hourly_data

    batch_size = 100 
    batches = [emails[i:i + batch_size] for i in range(0, len(emails), batch_size)]

    weekday_data = [0] * 7
    hourly_data = [0] * 24

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(process_batch, batches)
        for wd, hd in results:
            weekday_data = [sum(x) for x in zip(weekday_data, wd)]
            hourly_data = [sum(x) for x in zip(hourly_data, hd)]

    return jsonify({
        'weekdayData': weekday_data,
        'hourlyData': hourly_data
    })

@emails_bp.route("/top-senders")
@cross_origin(origins=["https://localhost:5173"], supports_credentials=True)
def get_top_senders():
    response, status_code = get_inbox()
    
    if status_code != 200:
        return jsonify({"error": "Failed to fetch emails"}), status_code

    emails = response.json

    if not emails:
        return jsonify({
            'senders': [],
            'counts': []
        })

    try:
        senders = [email.get('from', '').split('<')[-1].split('>')[0] for email in emails]
        sender_counts = Counter(senders)
        top_senders = sender_counts.most_common(10)

        return jsonify({
            'senders': [sender for sender, _ in top_senders],
            'counts': [count for _, count in top_senders]
        })
    except Exception as e:
        print(f"Error processing top senders: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred while processing emails'}), 500


@emails_bp.route('/logout')
def logout():
    session.clear()
    return flask.redirect('https://localhost:5173')
