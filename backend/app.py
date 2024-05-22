from flask import Flask, jsonify, request, make_response, session, redirect, render_template, url_for
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from api import login_bp, register_bp, emails_bp
from db import db
from dotenv import load_dotenv
import ssl
import os
from flask_vue import Vue

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
app.template_folder = '../frontend/src/views'

Vue(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db.init_app(app)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


@app.route("/")
def home():
    if not session.get('logged_in'):
        return "not logged in"
    else:
        return "logged in"
    
@app.route('/scrape')
def scrape():
    if not session.get('credentials'):
        return redirect(url_for('login.login_oauth'))

    # Render the ScrapePage.vue component as a template
    return render_template('ScrapePage.vue', username=session.get('username'))
    # return jsonify({"message":" login success"})

app.register_blueprint(login_bp,url_prefix="/authentication")
app.register_blueprint(register_bp,url_prefix="/authentication")
app.register_blueprint(emails_bp, url_prefix="/mail")

if __name__ == '__main__':
    CORS(app, resources={r"*": {"origins": "*"}})

    # context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=("C:\\emailscraper\\backend\\cert.pem", "C:\\emailscraper\\backend\\key.pem"))