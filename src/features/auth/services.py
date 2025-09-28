from bcrypt import checkpw
import jwt
import datetime
from flask import current_app


def generate_token(user_id):
    exp = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({
        'exp': exp,
        'sub': str(user_id),
    }, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
    return token if isinstance(token, str) else token.decode('utf-8')


def verify_user_password(hashed_password, password):
    return checkpw(
        password.encode('utf-8'),
        hashed_password.encode('utf-8'),
    )
