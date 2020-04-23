from flask import Blueprint, render_template, url_for, redirect, session, abort
from flask_login import login_required, current_user
from social.components.post.form import PostCreate, PostEdit
from social.models import Post
from slugify import slugify
from social import db

post_bp = Blueprint('post',__name__,template_folder='templates')

@post_bp.route('/create',methods=["GET","POST"])
@login_required
def create():
    form = PostCreate()
    if form.validate_on_submit():
        post = Post(form.title.data,form.text.data,current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html',form=form)

@post_bp.route('/view/<slug>')
def view(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template('view_post.html',post=post)

@post_bp.route('/edit/<int:id>',methods=["GET","POST"])
@login_required
def update(id):
    post = Post.query.filter_by(id=id).first_or_404()
    form = PostEdit()
    if form.validate_on_submit():
        post.title = form.title.data
        post.text = form.text.data
        post.slug = slugify(form.title.data)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('post.update',id=post.id))

    if post.user.id == current_user.id:
        form.text.data = post.text
        form.title.data = post.title
        return render_template('edit.html',post=post,form=form)
    else:
        return "access denied!"

@post_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.filter_by(id=id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))
