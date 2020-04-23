from flask import Blueprint, redirect, render_template, url_for, abort
from flask_login import current_user, login_required
from services.components.posts.form import CreateForm, EditForm
from slugify import slugify
from services.models import Post, User
from services import db

posts = Blueprint('posts',__name__)

@posts.route('/account/<int:id>')
def account(id):
    posts = Post.query.filter_by(user_id=id).all()
    user = User.query.get(id)
    return render_template('posts/account.html',posts=posts,user=user)

@posts.route('/create',methods=['GET','POST'])
@login_required
def create():
    form = CreateForm()
    if form.validate_on_submit():
        post = Post(form.title.data,form.text.data,current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('posts/create.html',form=form)

@posts.route('/view/<slug>')
def view(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('posts/view.html',post=post)

@posts.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit(id):
    form = EditForm()
    post = Post.query.get(id)
    if post.user.id != current_user.id:
        abort(404)

    if form.validate_on_submit():
        if post.title != form.title.data:
            post.title = form.title.data
            post.slug = slugify(form.title.data)
        post.text = form.text.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.edit',id=post.id))

    form.title.data = post.title
    form.text.data = post.text
    return render_template('posts/edit.html',form=form)

@posts.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post.user.id != current_user.id:
        abort(404)

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))

