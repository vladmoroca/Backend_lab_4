from ..db import db


class categoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(128), unique = True, nullable = False)
    user_id = db.Column(db.String, db.ForeignKey("user.id"), unique=False, nullable=True)

    record = db.relationship("recordModel", back_populates = "category", lazy = "dynamic")
    user = db.relationship("userModel", back_populates="category")