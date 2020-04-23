from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired
from wtforms import ValidationError
from social.models import User

class RegisterForm(FlaskForm):
    email = StringField('Email address',validators=[DataRequired(),Email()])
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('password_confirm',message='Passwords must match.')])
    password_confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')

