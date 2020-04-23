import os
from dotenv import load_dotenv
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy, get_debug_queries
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from services.blacklists import blacklists
from marshmallow import ValidationError

#load .env
load_dotenv()
load_dotenv(verbose=True)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)
Migrate(app,db)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklists

@app.errorhandler(ValidationError)
def error_handler(err):
    return err.messages, 400

@app.after_request
def sql_debug(response):
    queries = list(get_debug_queries())
    if queries:
        query_str = ''
        total_duration = 0.0
        for q in queries:
            total_duration += q.duration
            query_str += f'Query: {q.statement}\nDuration: {round(q.duration * 1000, 2)}ms\n'

        print('=' * 80)
        print('SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
        print('=' * 80)
        print(query_str.rstrip('\n'))
        print('=' * 80)

    return response
