from flask import render_template, redirect, url_for, Blueprint, request, abort, flash
from flask_login import login_user, logout_user
from is_safe_url import is_safe_url
from services.components.users.form import LoginForm, RegisterForm
from services.models import User
from services import db

user = Blueprint('user',__name__)

@user.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_pass(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next and not is_safe_url(next,{"localhost:5000"}):
                return abort(404)
            return redirect(next or url_for('index'))
        else:
            flash('Username or password wrong!')
            return redirect(url_for('user.login'))
    return render_template('users/login.html',form=form)

@user.route('/register',methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.email.data,form.username.data,form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('users/register.html',form=form)

@user.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
