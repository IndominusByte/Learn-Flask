'''
user one to many job
user one to many applicant

job one to one OverallScore
job one to many applicant

applicant one to many experience
applicant one to many education
'''
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100),unique=True,index=True)
    email = db.Column(db.String(100),unique=True,index=True)
    password = db.Column(db.String(100))
    avatar = db.Column(db.String(100),default='default.png')
    status = db.Column(db.Integer,default=0)
    token = db.Column(db.String(100))
    member = db.Column(db.String(64),default='free')
    crawler = db.Column(db.Integer,default=1)
    company_name = db.Column(db.String(100),nullable=True)
    company_site = db.Column(db.String(100),nullable=True)
    position = db.Column(db.String(100),nullable=True)
    created_at = db.Column(db.DateTime,default=datetime.now)
    updated_at = db.Column(db.DateTime,default=datetime.now)

    job = db.relationship('Job',backref='user',lazy='dynamic',cascade='all, delete, delete-orphan')
    applicant = db.relationship('Applicant',backref='user',lazy='dynamic',cascade='all, delete, delete-orphan')

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(100))
    image = db.Column(db.String(100))
    title_job = db.Column(db.String(100))
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    posted = db.Column(db.String(64))
    desc = db.Column(db.Text)
    concepts = db.Column(db.Text)
    keywords = db.Column(db.Text)
    created_at = db.Column(db.DateTime,default=datetime.now)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    overall_score = db.relationship('OverallScore',backref='job',uselist=False,cascade='all, delete, delete-orphan')
    applicant = db.relationship('Applicant',backref='job',lazy='dynamic',cascade='all, delete, delete-orphan')


class OverallScore(db.Model):
    __tablename__ = 'overall_scores'

    id = db.Column(db.Integer,primary_key=True)
    experience = db.Column(db.Integer)
    skills = db.Column(db.Integer)
    education = db.Column(db.Integer)
    accomplish = db.Column(db.Integer)
    licenses = db.Column(db.Integer)

    job_id = db.Column(db.Integer,db.ForeignKey('jobs.id'),nullable=False)

class Applicant(db.Model):
    __tablename__ = 'applicants'

    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(100))
    image = db.Column(db.Text)
    name = db.Column(db.String(100))
    languages = db.Column(db.String(100))
    title = db.Column(db.Text)
    score = db.Column(db.Float(precision=10,decimal_return_scale=2))
    verify = db.Column(db.String(100),default='disqualify')
    year_work = db.Column(db.Float(precision=10,decimal_return_scale=2))
    licenses =  db.Column(db.Text)
    skills = db.Column(db.Text)
    awards = db.Column(db.Text)
    created_at = db.Column(db.DateTime,default=datetime.now)

    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    job_id = db.Column(db.Integer,db.ForeignKey('jobs.id'),nullable=False)
    experience = db.relationship('Experience',backref='applicant',lazy='dynamic',cascade='all, delete, delete-orphan')
    education = db.relationship('Education',backref='applicant',lazy='dynamic',cascade='all, delete, delete-orphan')

class Experience(db.Model):
    __tablename__ = 'experiences'

    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100))
    company = db.Column(db.String(100))
    started = db.Column(db.String(64))
    year = db.Column(db.String(64))
    desc = db.Column(db.Text)

    applicant_id = db.Column(db.Integer,db.ForeignKey('applicants.id'),nullable=False)

class Education(db.Model):
    __tablename__ = 'educations'

    id = db.Column(db.Integer,primary_key=True)
    university = db.Column(db.String(100))
    major = db.Column(db.Text)
    year = db.Column(db.String(64))

    applicant_id = db.Column(db.Integer,db.ForeignKey('applicants.id'),nullable=False)

class JobPortal(db.Model):
    __tablename__ = 'job_portals'

    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(100),unique=True,index=True)
    image = db.Column(db.String(100),default='default.png')
    name = db.Column(db.String(100))
    corporation = db.Column(db.String(100))
    status = db.Column(db.String(100),default='has been requested.')
    created_at = db.Column(db.DateTime,default=datetime.now)
