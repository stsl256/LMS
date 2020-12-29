import random
import string
import json
from flask import Response
from Domain.Users import User
from Domain.Students import Student

def get_response(answer):
    js = json.dumps(answer)
    return Response(js, status=200, mimetype='application/json')

def generate_validation_code(N=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))

def blank_resp():
    return {
        'data': [],
        'error_message': '',
        'status': 'ok'
    }

def init_user(form):
    return User(
        name=form.name.data,
        surname=form.surname.data,
        second_name=form.second_name.data,
        status=form.status.data,
        registration_uid=generate_validation_code()
    )

def init_student(form, user_id):
    return Student(
        user_id=user_id,
        group_id=form.group_id.data,
        year=form.year.data,
        degree=form.degree.data,
        education_form=form.education_form.data,
        education_basis=form.education_basis.data
    )