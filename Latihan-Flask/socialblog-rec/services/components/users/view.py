import os, random, string
from flask import Blueprint, url_for, render_template, redirect, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from services import db, basedir
from services.models import User
from services.components.users.form import RegisterForm, LoginForm, UpdateProfile
from werkzeug.utils import secure_filename
from is_safe_url import is_safe_url

users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.username.data,form.email.data,form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    return render_template('users/register.html',form=form)

@users.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user.check_pass(form.password.data):
            next = request.args.get('next')
            if next and not is_safe_url(next,{'localhost':'5000'}):
                return abort(404)
            login_user(user)
            return redirect(next or url_for('index'))
        else:
            form.email.errors = ['password wrong!']
    return render_template('users/login.html',form=form)

@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateProfile()
    if form.validate_on_submit():
        redacted = True
        user = User.query.get(current_user.id)
        if form.upload.data:
            f = form.upload.data
            f.seek(0, os.SEEK_END)
            size = f.tell()
            if size < 300000:
                ext = f.filename.split('.')[-1]
                filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)) + '.' + ext
                if user.avatar != 'default.png': os.remove(os.path.join(basedir,'static/avatar/',user.avatar))
                f.seek(0)
                f.save(os.path.join(basedir,'static/avatar/',filename))
                f.close()
                user.avatar = filename
            else:
                redacted = False
                form.upload.errors = ['File size can only 300kb']
        user.username = form.username.data
        db.session.add(user)
        db.session.commit()
        if redacted: return redirect(url_for('users.account'))

    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('users/account.html',form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
