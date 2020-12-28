import json

from flask import Flask, request, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import Form, StringField, PasswordField, validators

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from Domain.Users import User
from Domain.Courses import Course
from Domain.Students import Student, Group
from Domain.Teachers import Teacher

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    name = StringField('Name', [validators.Length(min=3, max=35)])
    surname = StringField('Surname', [validators.Length(min=3, max=35)])
    second_name = StringField('Surname', [validators.Length(min=3, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired()
    ])

def blank_resp():
    return {
        'data': [],
        'error_message': '',
        'status': 'ok'
    }

def register_user_in(form):
    u = User(username=form.username.data,
             email=form.email.data,
             name=form.name.data,
             surname=form.surname.data,
             second_name=form.second_name.data)
    db.session.add(u)
    db.session.commit()
    return 0


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/register', methods=['POST'])
def register_user():
    answer = blank_resp()
    form = RegistrationForm(request.form)
    if form.validate():
        register_user_in(form)
    else:
        answer['status'] = 'error'
        answer['error_message'] = str(form.errors.items())

    js = json.dumps(answer)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/get_all_users', methods=['GET'])
def get_all_users():
    answer = blank_resp()

    try:
        answer['data'] = str(User.query.all())
    except Exception as e:
        answer['error_message'] = str(e)

    js = json.dumps(answer)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run()