import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

login_manager.login_view = "login.login"
login_manager.session_protection = "strong"

from social.components.login.view import login_bp
from social.components.register.view import register_bp
from social.components.account.view import account_bp
from social.components.post.view import post_bp

app.register_blueprint(login_bp)
app.register_blueprint(register_bp)
app.register_blueprint(account_bp,url_prefix='/account')
app.register_blueprint(post_bp,url_prefix='/post')
