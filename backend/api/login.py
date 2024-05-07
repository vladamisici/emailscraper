from flask import Blueprint, request, jsonify, render_template, redirect, url_for, session
import jwt
from models.user import User
from werkzeug.security import check_password_hash
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_ID = '339144602283-s2b47qd4vh5hk8ksu68as6b2lp8v1g5d.apps.googleusercontent.com'
CLIENT_SECRET = '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'
CLIENT_SECRET_FILE = "client_secret_email.json"
AUTH_URL = 'http://localhost'

SCOPES = ["https://mail.google.com/"]

login_bp = Blueprint('login', __name__, url_prefix='/login')

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
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES
    )
    flow.redirect_uri = url_for('.callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        prompt='select_account'
    )
    session['state'] = state
    return redirect(authorization_url)

@login_bp.route('/callback')
def callback():
    if request.args.get('state') != session.pop('state', None):
        return 'Invalid state', 400
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, scopes=SCOPES
    )
    flow.redirect_uri = url_for('.callback', _external=True)

    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    session['credentials'] = credentials.to_json()

    return redirect(url_for('index'))

@login_bp.route('/logout')
def logout():
    session.pop('credentials', None)
    return redirect(url_for('index'))