import os
from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
google_bp = make_google_blueprint(scope=["profile","email"])
app.register_blueprint(google_bp,url_prefix='/login')

@app.route('/')
def index():
    resp = google.get("/oauth2/v1/userinfo")
    return render_template('home.html')

@app.route('/welcome')
def welcome():
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    email= resp.json()["email"]
    return render_template('welcome.html',email=email)

@app.route('/login/google')
def login_google():
    if not google.authorized:
        return redirect(url_for('google.login'))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    return "You are {email} on Google".format(email=resp.json()["email"])

if __name__ == '__main__':
    app.run(debug=True)
