from functools import wraps
from flask import request, jsonify, current_app
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from flask import g


def _get_token():
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1].strip()
    cookie_token = request.cookies.get('accessToken')
    if cookie_token and cookie_token.startswith('Bearer '):
        return cookie_token.split(' ')[1].strip()
    return None


def require_authentication(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.method == "OPTIONS":
            return '', 204

        token = _get_token()
        if not token:
            return jsonify({'error': 'Token is missing or invalid'}), 401

        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            g.token_payload = payload
        except ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(*args, **kwargs)
    return decorated
