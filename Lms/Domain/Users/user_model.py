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
    status = db.Column(db.String(64))
    student = db.relationship('Student', backref='user', uselist=False)
    teacher = db.relationship('Teacher', backref='user', uselist=False)
    phone = db.Column(db.String(64))
    city = db.Column(db.String(64))
    description = db.Column(db.String(256))

    def __repr__(self):
        return '| Id: {id}, ' \
               'Логин: {username}, ' \
               'Email: {email}, ' \
               'ФИО: {surname} {name} {second_name}, ' \
               'Телефон: {phone}, Город: {city}, ' \
               'Описание: {descripption} |'.format(
            username=self.username, email=self.email, name=self.name,
            second_name=self.second_name, surname=self.surname, id=self.id,
            phone=self.phone, city=self.city, descripption=self.description
        )

    def get_user_id(self):
        return self.id

    def get_status(self):
        return self.status

    def get_registration_uid(self):
        return self.registration_uid

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email

    def set_personal_info(self, phone, city, description):
        self.phone = phone
        self.city = city
        self.description = description

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_uid():
        return str(uid())
