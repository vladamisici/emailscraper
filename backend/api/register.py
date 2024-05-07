from flask import Blueprint, jsonify, request
import jwt
from models.user import User

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = User.get_user_by_username(username=data.get('username'))

    if username is not None:
        return jsonify({"error":"Username already in use"}),409
    
    new_user = User(
        username=data.get('username'),
        email = data.get('email'),
        password = User.hash_password(data.get('password'))
    )
    print(new_user.password)
    new_user.save()
    return jsonify({"message":"user created"})
    
    