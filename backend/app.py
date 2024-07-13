from flask import Flask, jsonify, request, make_response, session
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from api import login_bp, register_bp, emails_bp
from db import db
from dotenv import load_dotenv
import ssl
import os

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "https://localhost:5173"}}, supports_credentials=True)

# CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_sessions')
# app.config['SESSION_FILE_THRESHOLD'] = 100

# app.session_interface = SecureCookieSessionInterface()

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    # SESSION_COOKIE_SAMESITE='Lax',
    # SECRET_KEY=os.getenv('SECRET_KEY')
)

# @app.after_request
# def after_request(response):
#     response.headers['Access-Control-Allow-Origin'] = 'https://localhost:5173'
#     response.headers['Access-Control-Allow-Credentials'] = 'true'
#     print(f"Session after request: {session}")
#     return response

db.init_app(app)

@app.route("/")
def home():
    if not session.get('logged_in'):
        return "not logged in"
    else:
        return "logged in"

app.register_blueprint(login_bp,url_prefix="/authentication")
app.register_blueprint(register_bp,url_prefix="/authentication")
app.register_blueprint(emails_bp, url_prefix="/mail")

if __name__ == '__main__':
    # context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('cert.pem', 'key.pem')
    # app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("C:\\emailscraper\\backend\\cert.pem", "C:\\emailscraper\\backend\\key.pem"))
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("C:\\Windows\\System32\\localhost+2.pem", "C:\\Windows\\System32\\localhost+2-key.pem"))