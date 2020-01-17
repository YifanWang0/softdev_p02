from flask import Flask, Blueprint, session, render_template, flash, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from utl.forms import SignUpForm, LogInForm, SearchForm
from flask_sqlalchemy import SQLAlchemy
import os, json

from datetime import datetime, timedelta

from utl.models import db, User, Group, GroupLinks, Task

'''
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store, flags)
'''

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

# start database
db.init_app(app)

with app.app_context():
    db.create_all()

# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please Log In to view this page!'
login_manager.login_message_category = 'danger'

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('home.html')


def missing_keys():
    for service in keys:
        if keys[service] == 'YOUR_API_KEY_HERE':
            flash('Key for {} is missing. See README.md for specific instructions.'.argsat(service), 'error')
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
        print("ahh")
        to_validate = User.query.filter_by(username=log_in_form.username.data).first()

        if to_validate is None or to_validate.password != log_in_form.password.data:
            print("BOOO")
            flash('Incorrect username or password!', 'danger')
        else:
            print("ahhhh")
            login_user(to_validate)

            if 'next' in session:
                return redirect(session['next'])
            else:
                flash('Logged in successfully!', 'success')
                return redirect(url_for('day'))

    return render_template('login.html', form=log_in_form)


@login_required
@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


@login_required
@app.route('/day', methods=['GET', 'POST'])
def day():
    today = datetime.today()
    weekday = today.weekday()
    tasks = {}
    personal_tasks = {}
    group_tasks = {}
    overdue_tasks = {}
    for day in range(weekday, 7):
        personal_tasks[days[day].capitalize() + "  " + (today + timedelta(day - weekday)).strftime('%x')[
                                                       0:5]] = Task.query.filter_by(user_id=current_user.id,
                                                                                    group_id=None,
                                                                                    due_date_m=int(
                                                                                        today.strftime('%m')),
                                                                                    due_date_d=int(today.strftime(
                                                                                        '%d')) + day - weekday
                                                                                    ).all()
    for day in range(weekday, 7):
        temp = {}
        for group in current_user.groups:
            if group != None:
                if (Task.query.filter_by(group_id=group.id,
                                         due_date_m=int(today.strftime('%m')),
                                         due_date_d=int(today.strftime('%d')) + day - weekday).count() > 0):
                    temp[group.name]=Task.query.filter_by(group_id=group.id,
                                                         due_date_m=int(today.strftime('%m')),
                                                         due_date_d=int(today.strftime('%d')) + day - weekday).all()
                else:
                    temp[group.name] = None
        group_tasks[days[day].capitalize() + "  " + (today + timedelta(day - weekday)).strftime('%x')[0:5]] = temp

    my_overdue_tasks = Task.query.filter(Task.group_id == None, Task.user_id == current_user.id,Task.due_date_m <= int(today.strftime('%m')),
                                         Task.due_date_d < int(today.strftime('%d'))).all()
    group_overdue_tasks = {}
    for group in current_user.groups:
        if group != None:
            group_overdue_tasks[group.name] = Task.query.filter(Task.group_id == group.id, Task.due_date_m <= int(today.strftime('%m')),
                                                                Task.due_date_d < int(today.strftime('%d'))).all()
        else:
            group_overdue_tasks[group.name] = None
    print(group_overdue_tasks)
    print(group_tasks)
    print(request.args)
    return render_template('week.html', personal_tasks=personal_tasks, group_tasks=group_tasks,
                           my_overdue_tasks=my_overdue_tasks, group_overdue_tasks=group_overdue_tasks,
                           editData=genEditCard(request.args))


@login_required
@app.route('/month', methods=['GET', 'POST'])
def month():
    today = datetime.today()
    weekday = today.weekday()
    print(genWeek(getWeek(today, weekday, 0)))
    print(today + timedelta(0))
    data = []
    data.append(genWeek(getWeek(today, weekday, 0)))
    data.append(genWeek(getWeek(today, weekday, 1)))
    data.append(genWeek(getWeek(today, weekday, 2)))
    data.append(genWeek(getWeek(today, weekday, 3)))
    return render_template('month.html', data=data, month=today.strftime('%B'),
                           displayData=genDisplayCard(request.args), editData=genEditCard(request.args))


def getWeek(today, weekday, weekIncrem):
    personal_tasks = {}
    group_tasks = {}
    today = today + timedelta(7 * weekIncrem)
    if weekday != 0:
        if weekday != 6:
            personal_tasks[days[6] + "," + (today + timedelta(-1 - weekday)).strftime('%m') + "," + (
                        today + timedelta(-1 - weekday)).strftime('%d')] = []
        else:
            personal_tasks[days[6] + "," + today.strftime('%m') + "," + today.strftime('%d')] = []
        group_tasks[days[6]] = []
        for i in range(0, weekday):
            personal_tasks[days[i] + "," + (today + timedelta(i - weekday)).strftime('%m') + "," + (
                        today + timedelta(i - weekday)).strftime('%d')] = []
            group_tasks[days[i]] = []
    else:
        today = today + timedelta(days=(6 - today.weekday() + (7 * weekIncrem)))
    for day in range(weekday, 6):
        personal_tasks[days[day] + "," + (today + timedelta(day - weekday)).strftime('%m') + "," + (
                    today + timedelta(day - weekday)).strftime('%d')] = Task.query.filter_by(user_id=current_user.id,
                                                                                             group_id=None,
                                                                                             due_date_m=int((
                                                                                                                        today + timedelta(
                                                                                                                    day - weekday)).strftime(
                                                                                                 '%m')),
                                                                                             due_date_d=int((
                                                                                                                        today + timedelta(
                                                                                                                    day - weekday)).strftime(
                                                                                                 '%d'))
                                                                                             ).all()
    # for day in range(weekday, 7):
    #     for group in current_user.groups:
    #         if group == None:
    #             break
    #         group_tasks[days[day]][group.name] = Task.query.filter_by(group_id=group.id,
    #                                                                   due_date_m=int(today.strftime('%m')),
    #                                                                   due_date_d=int(
    #                                                                       today.strftime('%d')) + day - weekday).all()
    return (personal_tasks, group_tasks)


def genWeek(data):
    personal_tasks = data[0]
    group_tasks = data[1]
    week = []
    for key in personal_tasks:
        day = [key.split(",")[1]]
        day.append(key.split(",")[2])
        temp = []
        for elem in personal_tasks[key]:
            temp.append(elem.title)
        for i in range(0, 3):
            if i < len(temp):
                day.append(temp[i])
            else:
                day.append("|")
        week.append(day)
    return week


def genDisplayCard(args):
    displayData = [1, [], ""]
    if len(args) == 0:
        return [0, [], ""]
    if len(args) == 1:
        return [2, [], ""]
    if (args['day'] == "" or args['month'] == ""):
        return [0, []]
    arr = Task.query.filter_by(user_id=current_user.id,
                               group_id=None,
                               due_date_m=int(args['month']),
                               due_date_d=int(args['day'])).all()
    displayData[1] = arr
    displayData[2] = "Tasks for: " + args['month'] + "/" + args['day']
    return displayData


def genEditCard(args):
    editData = {}
    print(args)
    if ('taskID' not in args):
        return {'id': "", 'title': "", 'description': "", 'dueDate': ""}
    selected = Task.query.filter_by(id=args['taskID']).first()
    editData['id'] = selected.id
    editData['title'] = selected.title
    editData['description'] = selected.description
    editData['dueDate'] = processNum(selected.due_date_m) + "/" + processNum(selected.due_date_d)
    print(editData)
    return editData


def processNum(n):
    if n > 9:
        return str(n)
    else:
        return "0" + str(n)


@login_required
@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    results = None

    if form.validate_on_submit():
        results = []
        search_string = form.search.data
        if search_string:
            if search_string == '':
                results = Group.query.all()
            else:
                results = Group.query.filter(
                    Group.name.like('%{}%'.format(search_string))).all()

    return render_template('search.html',
                           form=form,
                           query=form.search.data,
                           results=results)

@login_required
@app.route('/createrequests/<group_id>', methods=['POST'])
def request(group_id):
    group = Group.query.filter_by(id = int(group_id)).first()
    group.requests.append(current_user)
    db.session.commit()
    flash('You\'ve successfully requested to join the group!','success')
    return redirect(url_for('search'))

@login_required
@app.route("/requests" , methods=['GET','POST'])
def requests():
    groups = Group.query.filter_by(admin_id = current_user.id).all()
    requests = current_user.requests
    return render_template("requests.html",
                            groups = groups,
                            requests = requests)

@app.route("/accept/<group_id>/<requester_id>" , methods=['GET','POST'])
def accept(requester_id):
    group = Group.query.filter_by(id = int(group_id)).first()
    requester = User.query.filter_by(id = int(requester_id)).first()
    group.requesters.remove(requester)
    requester.groups.append(group)
    db.session.commit()

@app.route("/deny/<group_id>/<requester_id>" , methods=['GET','POST'])
def deny(group_id, requester_id):
    group = Group.query.filter_by(id = int(group_id)).first()
    requester = User.query.filter_by(id = int(requester_id)).first()
    group.requesters.remove(requester)
    db.session.commit()


@login_required
@app.route('/myGroups', methods=['GET', 'POST'])
def myGroups():
    print(current_user.username)
    print(current_user.groups)
    return render_template('mygroups.html',
                           groups=current_user.groups)


@login_required
@app.route('/leaveGroup/<group_id>', methods=['GET', 'POST'])
def leaveGroup(group_id):
    group = Group.query.filter_by(id=int(group_id)).first()
    current_user.groups.remove(group)
    db.session.commit()
    flash('You\'ve successfully left your group', 'success')
    return redirect(url_for('myGroups'))


@login_required
@app.route('/addTask', methods=['GET', 'POST'])
def addTask():
    print(request.args)
    if 'title' in request.args.keys() and 'description' in request.args.keys() and 'date' in request.args.keys() and 'time' in request.args.keys():
        print("YOO")
        date = request.args['date'].split("/")
        month = int(date[0])
        day = int(date[1])

        if 'time' in request.args and request.args['time'] is not None and request.args['time'] != '':
            time = request.args['time'].split(":")
            hour = int(time[0])
            min = int(time[1])
        else:
            hour = None
            min = None
        if ('group' in request.args and request.args['group'] != "N/A"):
            group = Group.query.filter_by(name=request.args['group']).first()
            task = Task(current_user.id, month, day, hour, min, 0, request.args['title'], request.args['description'],
                        group.id)
            group.tasks.append(task)
            print(group.tasks)
        else:
            task = Task(current_user.id, month, day, hour, min, 0, request.args['title'], request.args['description'],
                        None)
        current_user.tasks.append(task)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('day'))


@login_required
@app.route('/joinGroup/<group_id>', methods=['POST'])
def joinGroup(group_id):
    group = Group.query.filter_by(id=int(group_id)).first()
    current_user.groups.append(group)
    db.session.commit()
    flash('You\'ve successfully joined the group!', 'success')
    return redirect(url_for('search'))


@login_required
@app.route('/createGroup', methods=['POST'])
def createGroup():
    if 'name' in request.form.keys() and 'description' in request.form.keys():
        print("creating group")
        private = False
        for group in Group.query.all():
            print(group.name)
            print(request.form['name'])
            if group.name == request.form['name']:
                flash('You\'re group name already exists!', 'danger')
                return redirect(url_for('search'))

        if 'private' in request.form.keys() and request.form['private'] is not None:
            private = True
            print("private")
        group = Group(request.form['name'], current_user.id, request.form['description'], private)
        # for group in current_user.groups:
        #     print(loggin.info(current_user.group))
        db.session.add(group)
        db.session.commit()
        group = Group.query.filter_by(name=request.form['name']).first()
        current_user.groups.append(group)
        db.session.commit()
        flash('You\'ve successfully created your group', 'success')
    # if 'group name' in title.args.keys():
    #     Group.query.filter_by(id = 2)
    return redirect(url_for('search'))


@app.route('/deleteTask/<task_id>', methods=['GET', 'POST'])
def deleteTask(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    flash('You\'ve successfully completed your task', 'success')
    print(request.args)
    return redirect(url_for('day'))


@app.route('/editTask/<task_id>', methods=['GET', 'POST'])
def editTask(task_id):
    print(request.args)
    sel = Task.query.filter_by(id=task_id).first()
    date = request.args['date'].split("/")
    month = int(date[0])
    day = int(date[1])
    sel.title = request.args['title']
    sel.description = request.args['description']
    sel.due_date_m = month
    sel.due_date_d = day
    print()
    print(sel)
    db.session.commit()
    return redirect(url_for(request.args['originalPage']))


@app.route('/editGroup', methods=['GET', 'POST'])
def editGroup():
    return "f"


if __name__ == "__main__":
    app.debug = True
    app.run()
