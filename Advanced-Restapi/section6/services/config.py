from flask import Flask
from flask_sqlalchemy import SQLAlchemy, get_debug_queries
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from marshmallow import ValidationError
from services.blacklist import blacklist
from services.settings import Development
from dotenv import load_dotenv
from pathlib import Path  # python3 only

# Load .env
load_dotenv()
load_dotenv(verbose=True)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
app.config.from_object(Development())

CORS(app)
db = SQLAlchemy(app)
Migrate(app,db)
bcrypt = Bcrypt(app)
api = Api(app)
jwt = JWTManager(app)
oauth = OAuth(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

@app.errorhandler(ValidationError)
def error_handler(err):
    return err.messages, 400


if app.debug:
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
