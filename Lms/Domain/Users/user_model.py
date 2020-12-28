from app import db
from uuid import uuid4 as uid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from Domain.Teachers import Teacher
from Domain.Students import Student


class User(db.Model):
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
@@ -21,6 +23,12 @@ def __repr__(self):
        return '<User {username}, {name} {second_name} {surname}>'.format(username=self.username, name=self.name, second_name=self.second_name,
                                                                          surname=self.surname)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_uid():
        return str(uid())
