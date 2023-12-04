from sqlalchemy import func
from ..db import db


class recordModel(db.Model):
    __tablename__ = "record"

    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), unique=False, nullable=False)
    category_id = db.Column(db.String, db.ForeignKey("category.id"), unique=False, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    amount = db.Column(db.Float(precision=2), unique=False, nullable=False)

    user = db.relationship("userModel", back_populates="record")
    category = db.relationship("categoryModel", back_populates="record")

