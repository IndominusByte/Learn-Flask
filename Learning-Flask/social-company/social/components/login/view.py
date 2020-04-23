from flask import render_template, redirect, url_for, flash, Blueprint, request, abort
from social.components.login.form import LoginForm
from social.models import User
from flask_login import login_user
from is_safe_url import is_safe_url

login_bp = Blueprint('login',__name__,template_folder='templates')

@login_bp.route('/login',methods=["GET","POST"])
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
            return redirect(url_for('login.login'))
    return render_template('login.html',form=form)

