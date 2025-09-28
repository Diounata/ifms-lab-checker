from flask import Blueprint, jsonify, g
from features.auth.utils import require_authentication
from models.user import UserModel
from extensions import db

users_bp = Blueprint('users', __name__, url_prefix='/users')


@users_bp.route('/me', methods=['GET'])
@require_authentication
def get_authenticated_user():
    user_id = g.token_payload.get('sub')

    if not user_id:
        return jsonify({'error': 'Invalid token payload'}), 401

    user = UserModel.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({
        'user': {
            'id': user.user_id,
            'name': user.nome,
            'login': user.login,
            'type': user.tipo_usuario,
        }
    }), 200
