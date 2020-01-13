from flask import Flask, Blueprint, session, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_required,login_user, logout_user

from utl.forms import SignUpForm, LogInForm

import os, json

from utl.models import db, User, Group, GroupLinks

app = Flask(__name__)

DEBUG = True

# app configurations
app.config['SECRET_KEY'] = ('very secret key wow' if DEBUG else os.urandom(64))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
app.config['USE_SESSION_FOR_NEXT'] = True

keyfile = open('keys.json')
keys = json.load(keyfile)
googleCalendar_key = keys['google_calendar']
#set up login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return None
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'

db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('homepage.html')
def missing_keys():
    for service in keys:
        if keys[service] == 'YOUR_API_KEY_HERE':
            flash('Key for {} is missing. See README.md for specific instructions.'.format(service),'error')
    return render_template("homepage.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    sign_up_form = SignUpForm()

    if sign_up_form.validate_on_submit():
        print("YOO")
        # we just need to check that no accounts exist with the same username
        if User.query.filter_by(username=sign_up_form.username.data).first() is not None:
            flash('Username taken!', 'danger')
        else:
            # create the account
            print("YOO000")
            new_account = User(sign_up_form.username.data, sign_up_form.password.data)
            db.session.add(new_account)
            db.session.commit()

            flash('Account Created!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=sign_up_form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    log_in_form = LogInForm()

    if log_in_form.validate_on_submit():
        to_validate = User.query.filter_by(username=log_in_form.username.data).first()

        if to_validate is None or to_validate.password != log_in_form.password.data:
            flash('Incorrect username or password!', 'danger')
        else:
            login_user(to_validate)

            if 'next' in session:
                return redirect(session['next'])
            else:
                flash('Logged in successfully!', 'success')
                #return redirect(url_for('user.profile'))

    return render_template('login.html', form=log_in_form)


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/day')
def day():
    return render_template('day.html')

@app.route('/week')
def week():
    return render_template('week.html')

@app.route('/month')
def month():
    return render_template('month.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/requests')
def requests():
    return render_template('requests.html')

@app.route('/create')
def create():
    return "create"


if __name__ == "__main__":
    app.debug = True
    app.run()
