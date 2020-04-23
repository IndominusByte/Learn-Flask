from flask import render_template, redirect, url_for, Blueprint, abort
from flask_login import current_user
from services.components.posts.form import CrudForm
from slugify import slugify
from services.models import Post
from services import db

post = Blueprint('post',__name__)

@post.route('/create',methods=["GET","POST"])
def create():
    form = CrudForm()
    if form.validate_on_submit():
        post = Post(form.title.data,form.text.data,current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('posts/create.html',form=form)

@post.route('/edit/<int:id>',methods=["GET","POST"])
def edit(id):
    form = CrudForm()
    post = Post.query.filter_by(id=id).first_or_404()
    if post.user.id != current_user.id:
        return abort(404)

    if form.validate_on_submit():
        post.title = form.title.data
        post.slug = slugify(form.title.data)
        post.text = form.text.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.edit',id=post.id))

    form.title.data = post.title
    form.text.data = post.text

    return render_template('posts/edit.html',form=form)

@post.route('/view/<slug>')
def view(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('posts/view.html',post=post)
