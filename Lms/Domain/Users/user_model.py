from app import db, login
from uuid import uuid4 as uid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from Domain.Teachers import Teacher
from Domain.Students import Student

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    # personal
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    registration_uid = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    second_name = db.Column(db.String(64))
    student = db.relationship('Student', backref='user', uselist=False)
    teacher = db.relationship('Teacher', backref='user', uselist=False)
    # education
    group = db.Column(db.String(8))
    year = db.Column(db.Integer())
    degree = db.Column(db.String(16))
    education = db.Column(db.String(16))
    basis = db.Column(db.String(16))

    def __repr__(self):
        return '<User {username}, {name} {second_name} {surname}>'.format(
            username=self.username, name=self.name,
            second_name=self.second_name, surname=self.surname)
        
        def get_data(self):
        return 'Логин: {username}, ' \
               'Email: {email}, ' \
                                  'ФИО: {surname} {name} {second_name},' \
               'Учебная группа: {group}, Год поступления: {year}, Степень: {degree},' \
               'Форма обучения: {education}, Основа обучения: {basis}'.format(
            username=self.username, email=self.email, name=self.name,
            second_name=self.second_name, surname=self.surname,
            group=self.group, year=self.year, degree=self.degree, education=self.education,
            basis=self.basis
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_uid():
        return str(uid())
