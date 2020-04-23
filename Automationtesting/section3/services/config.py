import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SECRET_KEY = 'mysecret'
    JWT_SECRET_KEY = 'another-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Development(Config):
    DEBUG = True

class Production(Config):
    DEBUG = False
