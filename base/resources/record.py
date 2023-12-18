import datetime
import json
import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas.Schemas import recordSchema
from sqlalchemy.exc import IntegrityError
from ..models import *
from ..db import db

record_blueprint = Blueprint('record', __name__)

@record_blueprint.post("/record")
@jwt_required()
def create_record():
    user_id = get_jwt_identity()
    record_data = request.get_json()
    record_schema = recordSchema()
    try:
        validated_data = record_schema.load(record_data)
    except Exception as e:
        return "Incorrect record data", 400

    validated_data["id"] = uuid.uuid4().hex
    validated_data["created_at"] = datetime.datetime.now()
    category = categoryModel.query.get(record_data["category_id"])
    if category:
        validated_data["user_id"] = user_id
        validated_data["category_id"] = category.id
        record = recordModel(**validated_data)
    else:
        return "Incorrect category id", 400

    try:
        db.session.add(record)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "A record with this ID already exists", 400

    return validated_data

@record_blueprint.get("/record")
@jwt_required()
def get_records():
    user_id = get_jwt_identity()
    category_id = request.args.get("category_id")
    
    if user_id is None and category_id is None:
        return "Missing parameters", 400
    
    query = recordModel.query

    if category_id:
        query = query.filter_by(category_id=category_id)

    records_list = query.all()
    record_schema = recordSchema()
    return record_schema.dump(records_list, many=True)

@record_blueprint.delete("/record/<record_id>")
@jwt_required()
def record_delete(record_id):
    user_id = get_jwt_identity()
    record = recordModel.query.get(record_id)
    if record:
        if user_id == record.user_id:
            db.session.delete(record)
            db.session.commit()
            return "", 204
        else:
            return "it`s not your record", 403
    else:
        return "Record not found", 404