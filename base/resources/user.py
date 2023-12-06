import datetime
import uuid

from flask_jwt_extended import create_access_token, jwt_required

from ..models import userModel
from flask import jsonify, make_response, render_template, request, Blueprint
from ..schemas.Schemas import userSchema
from ..db import db
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256

user_blueprint = Blueprint('user', __name__)

@user_blueprint.post("/register")
def create_user():
    user_data = request.json
    user_schema = userSchema()
    try:
        validated_data = user_schema.load(user_data)
    except Exception as e:
        return "Incorrect user data", 400
    validated_data["id"] = uuid.uuid4().hex
    validated_data["password"] = pbkdf2_sha256.hash(validated_data["password"])
    user = userModel(**validated_data)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "A user with this name already exists", 400
    return validated_data

@user_blueprint.post("/login")
def login_user():
    user_data = request.json
    user_schema = userSchema()
    try:
        validated_data = user_schema.load(user_data)
    except Exception as e:
        return {"message": "Incorrect user data", "errors": e.messages}, 400

    user = userModel.query.filter_by(name=validated_data["name"]).first()

    if user and pbkdf2_sha256.verify(validated_data["password"], user.password):
        access_token = create_access_token(identity=user.id)
        return {"message": "Успішний вхід", "access_token": access_token}, 200

    return {"message": "Неправильне ім'я користувача або пароль"}, 401

@user_blueprint.delete("/user/<user_id>")
@jwt_required()
def user_delete(user_id):
    user = userModel.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return "", 204
    else:
        return "User not found", 404

@user_blueprint.get("/user/<user_id>")
@jwt_required()
def user_get(user_id):
    user = userModel.query.get(user_id)
    if user:
        user_schema = userSchema()
        return user_schema.dump(user)
    else:
        return "User not found", 404


@user_blueprint.get("/users")
@jwt_required()
def users_get():
    users_list = userModel.query.all()
    user_schema = userSchema()
    return user_schema.dump(users_list, many=True)


@user_blueprint.get("/healthcheck")
@jwt_required()
def healthcheck():
    time = datetime.datetime.now().isoformat()
    health = "It`s works!"
    data = {
        "time": time,
        "health": health
    }
    return jsonify(data)
