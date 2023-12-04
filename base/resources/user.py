import datetime
import uuid

from ..models import userModel
from flask import jsonify, request, Blueprint
from ..schemas.Schemas import userSchema
from ..db import db
from sqlalchemy.exc import IntegrityError

user_blueprint = Blueprint('user', __name__)

@user_blueprint.post("/user")
def create_user():
    user_data = request.args
    user_schema = userSchema()
    try:
        validated_data = user_schema.load(user_data)
    except Exception as e:
        return "Incorrect user data", 400
    validated_data["id"] = uuid.uuid4().hex
    user = userModel(**validated_data)
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "A user with this name already exists", 400
    return validated_data

@user_blueprint.delete("/user/<user_id>")
def user_delete(user_id):
    user = userModel.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return "", 204
    else:
        return "User not found", 404

@user_blueprint.get("/user/<user_id>")
def user_get(user_id):
    user = userModel.query.get(user_id)
    if user:
        user_schema = userSchema()
        return user_schema.dump(user)
    else:
        return "User not found", 404

@user_blueprint.get("/users")
def users_get():
    users_list = userModel.query.all()
    user_schema = userSchema()
    return user_schema.dump(users_list, many=True)

@user_blueprint.get("/healthcheck")
def healthcheck():
    time = datetime.datetime.now().isoformat()
    health = "It`s works!"
    data = {
        "time": time,
        "health": health
    }
    return jsonify(data)
