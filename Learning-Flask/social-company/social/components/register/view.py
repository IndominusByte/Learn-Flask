from flask import render_template, redirect, url_for, flash, Blueprint
from flask_login import login_user
from social.components.register.form import RegisterForm
from social.models import User
from social import db

register_bp = Blueprint('register',__name__,template_folder='templates')

@register_bp.route('/register',methods=["GET","POST"])
def register():
    form = RegisterForm();
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(email,username,password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login.login'))
    return render_template('register.html',form=form)
