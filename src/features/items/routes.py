from flask import Blueprint, request, jsonify, g
from features.auth.utils import require_authentication
from models.item import ItemModel
from extensions import db
from sqlalchemy import text
from models.evaluation import EvaluationModel, EvaluationChecklistModel

items_bp = Blueprint('items', __name__, url_prefix='/items')


@items_bp.route('/heritage/<string:heritage>', methods=['GET'])
@require_authentication
def get_item_by_heritage(heritage):
    item = ItemModel.query.filter_by(numero_patrimonio=heritage).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    sql = text(
        '''
        SELECT descricao, checklist_option_id
        FROM item_type_checklist_option
        JOIN checklist_options ON item_type_checklist_option.checklist_option_id = checklist_options.checklist_options_id
        WHERE item_type_checklist_option.item_type_id = :item_type_id
        ''')
    result = db.session.execute(sql, {'item_type_id': item.item_type_id})
    items = [{
        'description': row.descricao,
        'checklistOptionId': row.checklist_option_id
    } for row in result]

    return jsonify(
        {
            'id': item.item_id,
            'heritageNumber': item.numero_patrimonio,
            'description': item.descricao,
            'photoUrl': item.foto_url,
            'itemTypeId': item.item_type_id,
            'roomId': item.room_id,
            'checklists': items
        }
    ), 200


@items_bp.route('/evaluate/<string:heritage>', methods=['POST'])
@require_authentication
def evaluate_item(heritage):
    data = request.get_json()
    if not data or 'item_id' not in data or 'sala_id' not in data or 'checklists' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    item = ItemModel.query.filter_by(numero_patrimonio=heritage).first()
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    checklists = [
        EvaluationChecklistModel(
            checklist_option_id=checklist['checklist_option_id'],
            status=checklist['status']
        ) for checklist in data['checklists']
    ]

    evaluation = EvaluationModel(
        user_id=g.token_payload.get('sub'),
        item_id=data['item_id'],
        sala_id=data['sala_id'],
        data_hora=db.func.current_timestamp(),
        comentarios=data.get('comentarios', ''),
        checklist_entries=checklists
    )

    db.session.add(evaluation)
    db.session.commit()

    return jsonify({'message': 'Item evaluated successfully'}), 200
