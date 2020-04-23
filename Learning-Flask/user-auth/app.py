import os
from models import db, bycrpt, migrate, User, login_manager
from is_safe_url import is_safe_url
from form import LoginForm, RegisterForm
from flask import Flask, render_template, url_for, flash, request, abort, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate.init_app(app,db)
bycrpt.init_app(app)

login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=["GET","POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.email.data,form.username.data,form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully register!')
        return redirect(url_for('welcome'))
    return render_template('register.html',form=form)

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next and not is_safe_url(next,{"localhost:5000"}):
                return abort(404)
            flash(f'welcome back {user.username}')
            return redirect(next or url_for('welcome'))
        else:
            return 'gagal login'

    return render_template('login.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
