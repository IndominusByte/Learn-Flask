from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddOwner(FlaskForm):
    name = StringField('name of owner : ')
    id = IntegerField('id of puppy : ')
    submit = SubmitField()
