from flask import render_template, redirect, url_for, flash, Blueprint
from myproject.models import Puppy, db
from myproject.puppies.form import AddPuppy, DeletePuppy

puppies = Blueprint('puppies',__name__,template_folder='templates')

@puppies.route('/add',methods=["GET","POST"])
def AddPups():
    form = AddPuppy()
    if form.validate_on_submit():
        name = form.name.data
        pup = Puppy(name)
        db.session.add(pup)
        db.session.commit()
        flash('You successfully add puppy!')
        return redirect(url_for('puppies.list'))
    return render_template('puppies/add.html',form=form)

@puppies.route('/list')
def list():
    data = Puppy.query.all()
    return render_template('puppies/list.html',data=data)

@puppies.route('/delete',methods=["GET","POST"])
def delete():
    form = DeletePuppy()
    if form.validate_on_submit():
        id = form.id.data
        pup = Puppy.query.get(id)
        db.session.delete(pup)
        db.session.commit()
        flash('You successfully delete puppy')
        return redirect(url_for('puppies.list'))
    return render_template('puppies/delete.html',form=form)

