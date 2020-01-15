from flask import Flask, Blueprint, session, render_template, flash, redirect, url_for, request, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from utl.forms import SignUpForm, LogInForm, SearchForm

import os, json

from datetime import datetime

from utl.models import db, User, Group, GroupLinks, Task

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
# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


def missing_keys():
    for service in keys:
        if keys[service] == 'YOUR_API_KEY_HERE':
            flash('Key for {} is missing. See README.md for specific instructions.'.format(service), 'error')
    return render_template("home.html")


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
                return redirect(url_for('day'))

    return render_template('login.html', form=log_in_form)


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/day', methods=['GET', 'POST'])
def day():
    if 'user_id' not in session:
        flash('You must log in to access this page', 'warning')
        return redirect(url_for('index'))
    else:
        today = datetime.today()
        personal_tasks = Task.query.filter_by(user_id = current_user.id,
                                              group_id = None,
                                              due_date_m = int(today.strftime('%m')),
                                              due_date_dd = int(today.strftime('%d')),
                                              due_date_hr = int(today.strftime('%H'))
                                              )
        return render_template('day.html')


@app.route('/week', methods=['GET', 'POST'])
def week():
    return render_template('week.html')


@app.route('/month', methods=['GET', 'POST'])
def month():
    return render_template('month.html')


@app.route('/search', methods=['GET', 'POST'])
def search():

    form = SearchForm()

    results = None

    if form.validate_on_submit():
        results = []

        if form.data['search'] == '':
            qry = db_session.query(Album)
            results = qry.all()

        if not results:
            flash('No results found!')

    return render_template('search.html',
                           form=form,
                           query=form.search.data,
                           results=results)

@login_required
@app.route('/requests', methods=['GET', 'POST'])
def requests():
    return render_template('requests.html')

@login_required
@app.route('/myGroups', methods=['GET','POST'])
def myGroups():
    Group.query.filter_by()
    return render_template('mygroups.html')


@app.route('/leaveGroup', methods=['GET', 'POST'])
def leaveGroup():
    return "yo"

@app.route('/deleteTask', methods=['GET', 'POST'])
@app.route('/editTask', methods=['GET', 'POST'])
@app.route('/editGroup', methods=['GET', 'POST'])
@app.route('/Requests', methods=['GET'])
@app.route('/Requests', methods=['POST'])

@app.route('/addTask', methods=['GET','POST'])
def addTask():
    print(request.form['title'])
    if 'title' in request.form.keys() and 'description' in request.form.keys() and 'date'in request.form.keys() and 'time' in request.form.keys():
        print("YOO")
        date = request.form['date'].split("/")
        time = request.form['time'].split(":")
        month = int(date[0])
        day = int(date[1])
        hour = int(time[0])
        min = int(time[1])
        task = Task(month,day,hour,min,0,request.form['title'], request.form['description'])
        current_user.tasks.append(task)
        db.session.add(task)
        db.session.commit()
    return "add task"

@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
    print(request.form['title'])
    if 'title' in request.form.keys() and 'description' in request.form.keys() and 'date'in request.form.keys() and 'time' in request.form.keys():
        print("YOO")
        date = request.form['date'].split("/")
        time = request.form['time'].split(":")
        month = int(date[0])
        day = int(date[1])
        hour = int(time[0])
        min = int(time[1])
        task = Task(month,day,hour,min,0,request.form['title'], request.form['description'])
        current_user.tasks.append(task)
        db.session.add(task)
        db.session.commit()
    return "add event"

@app.route('/joinGroup', methods=['GET', 'POST'])
def joinGroup():
    if 'name' in request.form.keys() and 'description' in request.form.keys():
        Group.query.filter_by(id = int(request.form['group_name']))

@app.route('/createGroup', methods=['GET', 'POST'])
def createGroup():
    if 'name' in request.form.keys() and 'description' in request.form.keys():
        group = Group(request.form['name'],current_user.id, request.form['description'])
        current_user.append(group)
        db.session.add(group)
        db.session.commit()
if __name__ == "__main__":
    app.debug = True
    app.run()
