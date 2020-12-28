from app import db


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    description = db.Column(db.String(64))

    def __repr__(self):
        return '<Course {name}>'.format(name=self.name)