from flask import Blueprint, request, make_response
from .services import generate_token, verify_user_password
from models.user import UserModel
from datetime import datetime, timedelta


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('login') or not data.get('senha'):
        return make_response({'error': 'Missing credentials'}, 400)

    login = data.get('login')
    password = data.get('senha')

    user = UserModel.query.filter_by(login=login).first()
    if not user:
        return make_response({'error': 'User not found'}, 404)

    if verify_user_password(hashed_password=user.senha, password=password):
        token = generate_token(user_id=user.user_id)
        return make_response({'accessToken': token}, 200)
    return make_response({'code': 'invalid-credentials', 'message': 'Invalid credentials'}, 401)
