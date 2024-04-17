from flask import Blueprint, request, jsonify, render_template
import jwt
from models.user import User

login_bp = Blueprint('login', __name__, url_prefix='/login')

# @login_bp.route('/login')
# def login():
#     return jsonify({"message":"logged in"})

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.get_user_by_username(username=username)


    if user:
        if(User.check_password(user,password)):
            return jsonify({'message':'login succesful'}),200
        else:
            return jsonify({'error':'password incorrect'}),401
    else:
        return jsonify({'login error':'user not found'}),404