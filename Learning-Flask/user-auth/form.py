'''
string,password.submit
form -> register, login
'''
from models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Login!')

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Password must match!')])
    password2 = PasswordField('Password confirmation',validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('email already taken!')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('username already registered!')

