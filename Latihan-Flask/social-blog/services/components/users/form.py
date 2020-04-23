from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, EqualTo, DataRequired, Length
from wtforms import ValidationError
from services.models import User


class LoginForm(FlaskForm):
    email = StringField('Email address',validators=[Email(),DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField()

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email address',validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(),EqualTo('confirm',message='Password must match.'),Length(min=6)])
    confirm = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField()

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username hasbeen taken!')

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email hasbeen taken!')

