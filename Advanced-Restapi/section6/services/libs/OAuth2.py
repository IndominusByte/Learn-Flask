import os
from flask import session
from services.config import oauth

github = oauth.remote_app('github',
        base_url = 'https://api.github.com/',
        request_token_url = None,
        access_token_url = 'https://github.com/login/oauth/access_token',
        authorize_url = 'https://github.com/login/oauth/authorize',
        consumer_key = os.getenv('GITHUB_CLIENT_ID'),
        consumer_secret = os.getenv('GITHUB_CLIENT_SECRET'),)

@github.tokengetter
def get_github_token():
    if session.get('github_token'):
        return session.get('github_token')
