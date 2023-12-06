import os


FLASK_DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db?check_same_thread=False"
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")