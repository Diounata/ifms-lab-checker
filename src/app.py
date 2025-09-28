import os
from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import db
from models.checklist_option import ChecklistOptionModel
from models.evaluation import EvaluationModel
from models.user import UserModel
from models.room import RoomModel
from models.item import ItemModel
from features.auth.routes import auth_bp
from features.users.routes import users_bp
from features.rooms.routes import rooms_bp
from features.items.routes import items_bp


def create_app():
    app = Flask(__name__, static_folder='out', static_url_path='/')

    CORS(
        app,
        supports_credentials=True,
        origins="*",
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    )

    app.config.from_object(Config)

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(items_bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=4000)
