import json

from flask import Flask, request, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from wtforms import Form, StringField, PasswordField, validators
from flask_login import LoginManager, current_user, login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from utils import blank_resp, RegistrationForm, LoginForm
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
    user = User(username=form.username.data,
             email=form.email.data,
             name=form.name.data,
             surname=form.surname.data,
             second_name=form.second_name.data)
    db.session.add(u)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    return 0


@app.route('/')
@@ -71,12 +56,37 @@ def get_all_users():
    try:
        answer['data'] = str(User.query.all())
    except Exception as e:
        answer['status'] = 'error'
        answer['error_message'] = str(e)

    js = json.dumps(answer)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    answer = blank_resp()

    try:
        if current_user.is_authenticated:
            raise Exception('User is already authenticated')
        form = LoginForm(request.form)
        if form.validate():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                raise Exception('Invalid username or password')
            login_user(user)
        else:
            raise Exception(str(form.errors.items()))

    except Exception as e:
        answer['status'] = 'error'
        answer['error_message'] = str(e)

    js = json.dumps(answer)
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run()