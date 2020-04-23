import random, string, os
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from social.models import User, Post
from werkzeug.utils import secure_filename
from social.components.account.form import UpdateAccountForm
from social import basedir, db

account_bp = Blueprint('account',__name__,template_folder='templates')

@account_bp.route('/',methods=["GET","POST"])
@login_required
def account():
    form = UpdateAccountForm()
    form.email.data = current_user.email
    form.username.data = current_user.username
    user = User.query.get(current_user.id)
    if form.validate_on_submit():
        photo = form.upload.data
        filename = secure_filename(photo.filename)
        random_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(20)])
        filename = random_str + '.' + filename.split('.')[-1]
        photo.save(os.path.join(basedir,'static/avatar/',filename))
        user.email = form.email.data
        user.username = form.username.data
        user.avatar = filename
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('account.account'))
    return render_template('account.html',form=form)

@account_bp.route('/view/<int:id>')
def view(id):
    user = User.query.filter_by(id=id).first_or_404()
    posts = Post.query.filter_by(user_id=user.id).all()
    return render_template('view_account.html',user=user,posts=posts)
