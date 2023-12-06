from ..db import db
from passlib.hash import pbkdf2_sha256

class userModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(128), unique = True, nullable = False)
    password = db.Column(db.String, nullable=False)

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

    record = db.relationship("recordModel", back_populates = "user", lazy = "dynamic", cascade="all, delete-orphan")
    category = db.relationship("categoryModel", back_populates = "user", lazy = "dynamic", cascade="all, delete-orphan")

