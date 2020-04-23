'''
#Routing
/ , /add-pups, /list, /delete, /add-owner
#adding flash creating owners
#form
string , integer , submit
'''
import os
from flask import Flask, flash, render_template, redirect, url_for, session
from Form import AddOwner, AddPuppy, DeletePuppy
from Model import db, migrate, Owner, Puppy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app,db)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/add-pups',methods=['GET','POST'])
def AddPups():
    form = AddPuppy()
    if form.validate_on_submit():
        name = form.name.data
        pup = Puppy(name)
        db.session.add(pup)
        db.session.commit()
        flash('You successfully add puppy!')
        return redirect(url_for('list'))
    return render_template('addPups.html',form=form)

@app.route('/list')
def list():
    data = Puppy.query.all()
    return render_template('list.html',data=data)

@app.route('/delete',methods=['GET','POST'])
def delete():
    form = DeletePuppy()
    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()
        flash('You successfully delete puppy')
        return redirect(url_for('list'))
    return render_template('delete.html',form=form)

@app.route('/add-owner',methods=['GET','POST'])
def add_owner():
    form = AddOwner()
    if form.validate_on_submit():
        name = form.name.data
        id = form.id.data
        owner = Owner(name,id)
        db.session.add(owner)
        db.session.commit()
        flash(str(owner))
        return redirect(url_for('list'))
    return render_template('addOwner.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
