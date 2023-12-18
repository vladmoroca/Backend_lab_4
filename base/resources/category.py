import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..schemas.Schemas import categorySchema
from sqlalchemy.exc import IntegrityError
from ..models.category import categoryModel
from ..db import db

category_blueprint = Blueprint('category', __name__)

@category_blueprint.get("/category")
@jwt_required()
def categories_get():
    user_id = get_jwt_identity()
    categories_list = categoryModel.query.filter(categoryModel.user_id == user_id).all()
    categories_list.extend(categoryModel.query.filter(not categoryModel.user_id).all())
    schema = categorySchema()
    return schema.dump(obj=categories_list, many=True)

@category_blueprint.post("/category")
@jwt_required()
def create_category():
    user_id = get_jwt_identity()
    category_data = request.get_json()
    category_schema = categorySchema()
    try:
        validated_data = category_schema.load(category_data)
    except Exception as e:
        return "Incorrect category data", 400
    validated_data["id"] = uuid.uuid4().hex
    validated_data["user_id"] = user_id
    category = categoryModel(**validated_data)
    try:
        db.session.add(category)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "A category with this name already exists", 400
    return validated_data

@category_blueprint.delete("/category/<category_id>")
@jwt_required()
def category_delete(category_id):
    user_id = get_jwt_identity()
    category = categoryModel.query.get(category_id)
    if category:
        if(user_id != category.user_id):
            db.session.delete(category)
            db.session.commit()
            return "", 204
        else:
            return "it`s not your category"
    else:
        return "Category not found", 404