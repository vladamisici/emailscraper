from flask import Flask, jsonify, request, make_response, session
from flask_bcrypt import Bcrypt
from api import login_bp, register_bp, emails_bp
from db import db
from dotenv import load_dotenv
import ssl
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
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
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("C:\\emailscraper\\backend\\cert.pem", "C:\\emailscraper\\backend\\key.pem"))