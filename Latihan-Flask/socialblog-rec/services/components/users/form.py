from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Email, Length, EqualTo
from wtforms import ValidationError
from services.models import User

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[Required()])
    email = StringField('Email address',validators=[Required(),Email()])
    password = PasswordField('Password',validators=[Required(),Length(min=6),EqualTo('password2',message='Passwords must match.')])
    password2 = PasswordField('Confirm Password',validators=[Required(),Length(min=6)])
    submit = SubmitField('Register')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email address',validators=[Required(),Email()])
    password = PasswordField('Password',validators=[Required()])
    submit = SubmitField('Login')

    def validate_email(self,field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('data not found!')

class UpdateProfile(FlaskForm):
    username = StringField('Username',validators=[Required()])
    email = StringField('Email address')
    upload = FileField('Upload Profile Picture',validators=[FileAllowed(['jpg','png'],'.jpg and .png only!')])
    submit = SubmitField('Update profile')
