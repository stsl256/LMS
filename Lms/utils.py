from wtforms import Form, StringField, PasswordField, validators
from wtforms.validators import DataRequired, ValidationError
from Domain.Users import User

def blank_resp():
    return {
        'data': [],
        'error_message': '',
        'status': 'ok'
    }


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    name = StringField('Name', [validators.Length(min=3, max=35)])
    surname = StringField('Surname', [validators.Length(min=3, max=35)])
    second_name = StringField('Surname', [validators.Length(min=3, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired()
    ])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])