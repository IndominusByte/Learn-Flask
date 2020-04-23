from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from services.config import Development
from marshmallow import ValidationError

app = Flask(__name__)
app.config.from_object(Development)

db = SQLAlchemy(app)
Migrate(app,db)
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.errorhandler(ValidationError)
def errorhandler(err):
    return err.messages, 400
