from ..db import db


class userModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(128), unique = True, nullable = False)

    record = db.relationship("recordModel", back_populates = "user", lazy = "dynamic", cascade="all, delete-orphan")
    category = db.relationship("categoryModel", back_populates = "user", lazy = "dynamic", cascade="all, delete-orphan")

