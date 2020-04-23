from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired,Email

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(),Email()])
    upload = FileField('Upload Profile Picture',validators=[FileRequired(),FileAllowed(['jpg','png'],'Images only!')])
    submit = SubmitField()
