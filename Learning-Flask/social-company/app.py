'''
route -> home, about, logout, register, login
# MISS PAGINATION
'''
from social import app
from social.models import Post
from flask import render_template, redirect, url_for
from flask_login import logout_user, login_required

@app.route('/')
@app.route('/<int:page>')
def index(page=1):
    per_page = 1
    posts = Post.query.order_by(Post.id.desc()).paginate(page,per_page,error_out=False)
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='192.168.18.13',debug=True)
