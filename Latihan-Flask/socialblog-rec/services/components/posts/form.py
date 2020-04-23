from services.models import Post
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required
from wtforms import ValidationError

class CreateForm(FlaskForm):
    title = StringField('Title',validators=[Required()])
    text = TextAreaField('Text',validators=[Required()])
    submit = SubmitField()

    def validate_title(self,field):
        if Post.query.filter_by(title=field.data).first():
            raise ValidationError('cannot duplicate title!')

class EditForm(FlaskForm):
    title = StringField('Title',validators=[Required()])
    text = TextAreaField('Text',validators=[Required()])
    submit = SubmitField()
