from services import app
from services.models import Post
from flask import render_template

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('home.html',posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
