from extensions import db
from bcrypt import hashpw, gensalt


class UserModel(db.Model):
    __tablename__ = 'usuarios'

    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(40))
    senha = db.Column(db.String(60))
    nome = db.Column(db.String(100))
    tipo_usuario = db.Column(db.String(20))

    def __init__(self, login, senha, nome, tipo_usuario):
        self.login = login
        self.senha = hashpw(senha.encode('utf-8'), gensalt()).decode('utf-8')
        self.nome = nome
        self.tipo_usuario = tipo_usuario

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'nome': self.nome,
            'tipo_usuario': self.tipo_usuario
        }

    @classmethod
    def find_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(login=login).first()

    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()
