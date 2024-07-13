from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session, json, Flask
import jwt
from models.user import User
from werkzeug.security import check_password_hash
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import os
from flask_cors import CORS, cross_origin
from .scrape import emails_bp, get_inbox
import flask
import base64

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')

AUTH_URL = os.getenv('AUTH_URL')

SCOPES = ["https://mail.google.com/"]

login_bp = Blueprint('login', __name__)
# login_bp = Blueprint('login', __name__, url_prefix='/login')
CORS(login_bp, resources={r"*": {"origins": "https://localhost:5173"}}, supports_credentials=True)



@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.get_user_by_username(username=username)

    print(User.hash_password(password))
    if user:
        if(user.check_password(password)):
            return jsonify({'message':'login succesful'}),200
        else:
            return jsonify({'error':'password incorrect'}),401
    else:
        return jsonify({'login error':'user not found'}),404

@login_bp.route('/login_oauth', methods=['GET'])
def login_oauth():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES
    )
    flow.redirect_uri = url_for('.callback', _external=True, _scheme='https')
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='select_account'
    )
    session['state'] = state
    flask.session.modified = True
    # print(session)
    return flask.redirect(authorization_url)

@login_bp.route('/callback')
def callback():
    state = session.get('state')
    print(state)
    if not state or request.args.get('state') != state:
        return 'Invalid state', 400
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES
    )
    flow.redirect_uri = url_for('.callback', _external=True, _scheme='https')

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    # print("credentiale asddasd", json.dumps(credentials.to_json(), indent=2))
    # print(credentials.to_json())
    service = build('gmail', 'v1', credentials=credentials)
    profile = service.users().getProfile(userId='me').execute()
    session['email'] = profile['emailAddress']
    session['credentials'] = credentials_to_dict(credentials)
    # print(session)
    # return redirect(url_for('emails.get_inbox'))
    # return get_inbox()
    return redirect('https://localhost:5173/scrape')

def credentials_to_dict(credentials):
    return{
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def get_credentials():
    credentials = json.loads(session.get('credentials'))
    return credentials

@login_bp.route('/get_email', methods=['GET'])
def get_email():
    email_addr = session.get('email')
    if not email_addr:
        return jsonify({'error': 'Email not found'}), 404
    return jsonify({'email': email_addr}), 200
