from flask import flash, redirect, url_for, render_template, Blueprint
from myproject.owners.form import AddOwner
from myproject.models import db, Owner

owner = Blueprint('owner',__name__,template_folder='templates')

@owner.route('/add',methods=["GET","POST"])
def add():
    form = AddOwner()
    if form.validate_on_submit():
        name = form.name.data
        id = form.id.data
        owner = Owner(name,id)
        db.session.add(owner)
        db.session.commit()
        flash(str(owner))
        return redirect(url_for('puppies.list'))
    return render_template('add.html',form=form)

