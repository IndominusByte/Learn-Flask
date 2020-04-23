import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.session_protection = "strong"
login_manager.login_view = "user.login"

from services.components.users.views import user
from services.components.posts.views import post

app.register_blueprint(user,url_prefix='/user')
app.register_blueprint(post,url_prefix='/post')
