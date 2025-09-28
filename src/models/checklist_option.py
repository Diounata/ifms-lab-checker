from extensions import db


class ChecklistOptionModel(db.Model):
    __tablename__ = 'checklist_options'

    checklist_options_id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(255), nullable=False, unique=True)
    obrigatorio_descricao = db.Column(
        db.Boolean, nullable=False, default=False)

    def __init__(self, descricao, obrigatorio_descricao=False):
        self.descricao = descricao
        self.obrigatorio_descricao = obrigatorio_descricao

    def json(self):
        return {
            'checklist_options_id': self.checklist_options_id,
            'descricao': self.descricao,
            'obrigatorio_descricao': self.obrigatorio_descricao
        }

    @classmethod
    def find_option(cls, checklist_options_id):
        return cls.query.filter_by(checklist_options_id=checklist_options_id).first()

    def save_option(self):
        db.session.add(self)
        db.session.commit()

    def delete_option(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_option_by_description(cls, description):
        return cls.query.filter_by(descricao=description).first()
