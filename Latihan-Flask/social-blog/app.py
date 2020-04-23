from flask import render_template
from services import app
from services.models import Post

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('home.html',posts=posts)

if __name__ == '__main__':
    app.run(debug=True)
