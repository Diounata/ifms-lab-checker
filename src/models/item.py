from extensions import db


class ItemModel(db.Model):
    __tablename__ = 'itens'

    item_id = db.Column(db.Integer, primary_key=True)
    numero_patrimonio = db.Column(db.String(50), nullable=True)
    descricao = db.Column(db.String(255), nullable=False)
    foto_url = db.Column(db.String(255), nullable=True)

    item_type_id = db.Column(db.Integer, db.ForeignKey(
        'item_types.item_type_id'), nullable=False)

    room_id = db.Column(db.Integer, db.ForeignKey(
        'rooms.room_id'), nullable=True)

    def __init__(self, numero_patrimonio, descricao, foto_url=None, room_id=None, item_type_id=None):
        self.numero_patrimonio = numero_patrimonio
        self.descricao = descricao
        self.foto_url = foto_url
        self.room_id = room_id
        self.item_type_id = item_type_id
