from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField

class AddPuppy(FlaskForm):
    name = StringField('add name of puppy : ')
    submit = SubmitField()

class DeletePuppy(FlaskForm):
    id = IntegerField('delete puppy : ')
    submit = SubmitField()

class AddOwner(FlaskForm):
    name = StringField('name of owner : ')
    id = IntegerField('id of puppy : ')
    submit = SubmitField()
