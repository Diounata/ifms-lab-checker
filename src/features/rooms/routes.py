from flask import Blueprint, jsonify
from features.auth.utils import require_authentication
from models.room import RoomModel
from extensions import db

rooms_bp = Blueprint('rooms', __name__, url_prefix='/rooms')


@rooms_bp.route('/qrcode/<string:qr_code>', methods=['GET'])
@require_authentication
def get_room_by_qrcode(qr_code):
    room = RoomModel.query.filter_by(qr_code=qr_code).first()
    if not room: return jsonify({'error': 'Room not found'}), 404
    
    return jsonify(
        {
            'id': room.room_id,
            'name': room.nome,
            'descricao': room.descricao,
            'qrcode': room.qr_code,
            'type': room.tipo_sala,
        }    
    ), 200
