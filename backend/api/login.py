from flask import Blueprint, request, jsonify, render_template
import jwt

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/login')
def login():
    return jsonify({"message":"logged in"})

# @login_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     email = data.get('email')
#     password = data.get('password')

#     return jsonify({'message':'user succesfully registered'}), 201