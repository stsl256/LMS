from app import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    grade = db.Column(db.Integer)
    students = db.relationship('student', backref='group', lazy='dynamic')

    def __repr__(self):
        return "<Group {}>".format(self.name)
