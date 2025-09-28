from extensions import db


class RoomModel(db.Model):
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(255))
    qr_code = db.Column(db.String(255))
    tipo_sala = db.Column(db.String(50))

    def __init__(self, nome, descricao, qr_code, tipo_sala):
        self.nome = nome
        self.descricao = descricao
        self.qr_code = qr_code
        self.tipo_sala = tipo_sala

    def json(self):
        return {
            'room_id': self.room_id,
            'nome': self.nome,
            'descricao': self.descricao,
            'qr_code': self.qr_code,
            'tipo_sala': self.tipo_sala,
        }

    @classmethod
    def find_room(cls, room_id):
        return cls.query.filter_by(room_id=room_id).first()

    @classmethod
    def find_by_qr_code(cls, qr_code):
        return cls.query.filter_by(qr_code=qr_code).first()

    @classmethod
    def find_by_name(cls, nome):
        return cls.query.filter_by(nome=nome).first()

    def save_room(self):
        db.session.add(self)
        db.session.commit()

    def delete_room(self):
        db.session.delete(self)
        db.session.commit()
