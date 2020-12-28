from app import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    grade = db.Column(db.Integer)
    students = db.relationship('Student', backref='group', lazy='dynamic')

    def __repr__(self):
        return "<Group {}>".format(self.name)
