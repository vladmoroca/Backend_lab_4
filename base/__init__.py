from flask import Flask
from flask_migrate import Migrate
from base.db import db
from .resources.user import user_blueprint
from .resources.category import category_blueprint
from .resources.record import record_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)
    db.init_app(app)
    migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()
    
    app.register_blueprint(user_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(record_blueprint)
    return app
