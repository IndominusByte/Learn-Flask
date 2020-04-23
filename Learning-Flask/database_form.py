'''
#Database
puppies -> id,name
#Routing
/, /add, /list, /delete
#Form
AddForm, DeleteForm
'''
import os
from flask_wtf import FlaskForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for
from wtforms import StringField, IntegerField, SubmitField

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret' #for session and csrf token
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'database_form.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)

######## Setup form ########
class AddForm(FlaskForm):
    name = StringField('input your name puppies')
    submit = SubmitField()

class DeleteForm(FlaskForm):
    id = IntegerField('remove your puppies')
    submit = SubmitField()

######## SETUP DATABASE #######
class Puppy(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return f"name puppy is {self.name}"

@app.route('/')
def index():
    return render_template('database-views/home.html')

@app.route('/add', methods=['GET','POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        name = form.name.data
        pup = Puppy(name)
        db.session.add(pup)
        db.session.commit()
        return redirect(url_for('list'))

    return render_template('database-views/add.html',form=form)

@app.route('/delete', methods=['GET','POST'])
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()
        return redirect(url_for('list'))
    return render_template('database-views/delete.html',form=form)

@app.route('/list')
def list():
    data = Puppy.query.all()
    return render_template('database-views/list.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
