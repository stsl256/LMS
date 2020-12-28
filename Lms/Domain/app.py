import json
from flask import Flask, request, Response
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,\
    current_user, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

from utils import blank_resp, RegistrationForm, LoginForm, CourseForm
from Domain.Users import User
from Domain.Courses import Course
from Domain.Students import Student, Group
from Domain.Teachers import Teacher

def register_user_in(form):
    user = User(username=form.username.data,
             email=form.email.data,
             name=form.name.data,
             surname=form.surname.data,
             second_name=form.second_name.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()

def add_course_in(form):
    course = Course(name=form.name.data, description=form.name.data)
    db.session.add(course)
    db.session.commit()

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

@app.route('/logout')
def logout():
    answer = blank_resp()
    try:
        logout_user()
    except Exception as e:
        answer['status'] = 'error'
        answer['error_message'] = str(e)

    js = json.dumps(answer)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/create_course', methods=['GET', 'POST'])
@login_required
def create_course():
    """ Администратор может создать учебный курс, указав его название и текстовое описание.
    
    """
    answer = blank_resp()

    form = CourseForm(request.form)
    if form.validate():
        add_course_in(form)
    else:
        answer['status'] = 'error'
        answer['error_message'] = str(form.errors.items())

    js = json.dumps(answer)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/get_all_courses', methods=['GET'])
def get_all_courses():
    answer = blank_resp()

    try:
        answer['data'] = str(Course.query.all())
    except Exception as e:
        answer['status'] = 'error'
        answer['error_message'] = str(e)

    js = json.dumps(answer)
    resp = Response(js, status=200, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run()