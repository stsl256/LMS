from app import db
from Domain.Students import Group


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    year = db.Column(db.Integer)
    degree = db.Column(db.String(64))
    education_form = db.Column(db.String(64))
    is_contract = db.Column(db.Boolean)
