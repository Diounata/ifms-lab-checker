from extensions import db
from models.checklist_option import ChecklistOptionModel


class EvaluationChecklistModel(db.Model):
    __tablename__ = 'evaluation_checklist'

    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(
        db.Integer, db.ForeignKey('evaluations.evaluation_id'))
    checklist_option_id = db.Column(db.Integer, db.ForeignKey(
        'checklist_options.checklist_options_id'))
    status = db.Column(db.String(50), nullable=False)

    checklist_option = db.relationship(ChecklistOptionModel)


class EvaluationModel(db.Model):
    __tablename__ = 'evaluations'

    evaluation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'usuarios.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey(
        'itens.item_id'), nullable=False)
    sala_id = db.Column(db.Integer, db.ForeignKey(
        'rooms.room_id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    comentarios = db.Column(db.String(255), nullable=True)
    foto = db.Column(db.String(255), nullable=True)
    descricao_outros = db.Column(db.String(255), nullable=True)

    item = db.relationship('ItemModel', backref='evaluations')
    checklist_entries = db.relationship(
        'EvaluationChecklistModel',
        backref='evaluation',
        cascade="all, delete-orphan"
    )

    def __init__(self, user_id, item_id, sala_id, data_hora, comentarios=None, foto=None, checklist_entries=None, descricao_outros=None):
        self.user_id = user_id
        self.item_id = item_id
        self.sala_id = sala_id
        self.data_hora = data_hora
        self.comentarios = comentarios
        self.foto = foto
        self.checklist_entries = checklist_entries or []
        self.descricao_outros = descricao_outros

    def json(self):
        return {
            'evaluation_id': self.evaluation_id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'sala_id': self.sala_id,
            'data_hora': self.data_hora.isoformat(),
            'comentarios': self.comentarios,
            'foto': self.foto,
            'checklist': [
                {
                    'descricao': entry.checklist_option.descricao,
                    'status': entry.status
                } for entry in self.checklist_entries
            ],
            'descricao_outros': self.descricao_outros
        }

    @classmethod
    def find_evaluation(cls, evaluation_id):
        return cls.query.filter_by(evaluation_id=evaluation_id).first()

    def save_evaluation(self):
        db.session.add(self)
        db.session.commit()

    def delete_evaluation(self):
        db.session.delete(self)
        db.session.commit()
