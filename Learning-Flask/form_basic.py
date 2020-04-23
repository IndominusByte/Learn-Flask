from flask import Flask, render_template, redirect, url_for, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SelectField, RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = 'mysecretkey'

class Formfield(FlaskForm):
    name = StringField('input your name : ')
    submit = SubmitField()

class FormOne(FlaskForm):
    breed = StringField('What breed are you? ',validators=[DataRequired()])
    neutered = BooleanField('Have you been neutered? ')
    food = SelectField('Pick your facorite food',choices=[('ikan','Fish'),('daging','Meat'),('sayur','Vegetables')])
    mood = RadioField('Please choose your mood:',choices=[('mood_one','Happy'),('mood_two','Excited')])
    feedback = TextAreaField('Any other feedback')
    submit = SubmitField()

@app.route('/',methods=["GET","POST"])
def index():
    name = False
    form = Formfield()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template('form-basic/home.html',name=name,form=form)

@app.route('/form1', methods=['GET','POST'])
def form_one():
    form = FormOne()
    if form.validate_on_submit():
        data = {
            'breed':form.breed.data,
            'neutered':form.neutered.data,
            'food':form.food.data,
            'mood':form.mood.data,
            'feedback':form.feedback.data,
        }
        session['puppy'] = data
        flash('success filled out the puppy survey!')
        flash(data['breed'])

        return redirect(url_for('thankyou'))

    return render_template('form-basic/FormFieldOne.html',form=form)

@app.route('/thanyou')
def thankyou():
    return render_template('form-basic/thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
