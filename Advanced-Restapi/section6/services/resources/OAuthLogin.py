from flask import session
from flask_restful import Resource, url_for
from services.libs.OAuth2 import github

class GithubLogin(Resource):
    def get(self):
        return github.authorize(callback=url_for('github.authorize',_external=True))

class GithubAuthorize(Resource):
    def get(self):
        resp = github.authorized_response()
        if resp is None or not resp.get('access_token'):
            return {"error":resp['error'],"error_description":resp['error_description']},404

        session['github_token'] = resp['access_token']
        github_user = github.get('user')
        return github_user.data, 200
