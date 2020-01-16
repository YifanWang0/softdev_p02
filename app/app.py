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

days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

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
    for day in range(weekday,7):
        personal_tasks[days[day]] = Task.query.filter_by(user_id = current_user.id,
                                                        group_id = None,
                                                        due_date_m = int(today.strftime('%m')),
                                                        due_date_d = int(today.strftime('%d')) + day - weekday
                                                        ).all()
    for day in range(weekday,7):
        for group in current_user.groups:
            if group == None:
                break
            group_tasks[days[day]][group.name] = Task.query.filter_by(group_id = group.id,
                                                            due_date_m = int(today.strftime('%m')),
                                                            due_date_d=int(today.strftime('%d')) + day - weekday).all()
    return render_template('day.html', personal_tasks = personal_tasks, group_tasks = group_tasks)

@login_required
@app.route('/month', methods=['GET', 'POST'])
def month():
    today = datetime.today()
    weekday = today.weekday()
    print(genWeek(getWeek(today,weekday,0)))
    print(today + timedelta(0))
    firstRow=[0,1,2,3,4,5,6]
    secondRow=[7,8,9,10,11,12,13]
    thirdRow=[14,15,16,17,18,19,20]
    fourthRow=[21,22,23,24,25,26,28]
    data=[]
    data.append(genWeek(getWeek(today,weekday,0)))
    data.append(genWeek(getWeek(today,weekday,1)))
    data.append(genWeek(getWeek(today,weekday,2)))
    data.append(genWeek(getWeek(today,weekday,3)))
    # tempWeek={"date","tasks","events"}
    return render_template('month.html', data=data)

def getWeek(today,weekday,weekIncrem):
    personal_tasks = {}
    group_tasks = {}
    today=today+timedelta(7*weekIncrem)
    if weekday != 0:
        if weekday !=6:
            personal_tasks[days[6] + "," + (today + timedelta(-1-weekday)).strftime('%d')] = []
        else:
            personal_tasks[days[6] + "," + today.strftime('%d')] = []
        group_tasks[days[6]] = []
        for i in range(0,weekday):
            personal_tasks[days[i] + "," + (today + timedelta(i-weekday)).strftime('%d')] = []
            group_tasks[days[i]] = []
    else:
        today = today + timedelta(days=(6 - today.weekday() + (7 * weekIncrem)))
    for day in range(weekday, 6):
        personal_tasks[days[day] + "," + (today + timedelta(day-weekday)).strftime('%d')] = Task.query.filter_by(user_id=current_user.id,
                                                         group_id=None,
                                                         due_date_m=int((today + timedelta(day-weekday)).strftime('%m')),
                                                         due_date_d=int((today + timedelta(day-weekday)).strftime('%d'))
                                                         ).all()
    for day in range(weekday, 7):
        for group in current_user.groups:
            if group == None:
                break
            group_tasks[days[day]][group.name] = Task.query.filter_by(group_id=group.id,
                                                                      due_date_m=int(today.strftime('%m')),
                                                                      due_date_d=int(
                                                                          today.strftime('%d')) + day - weekday).all()
    return(personal_tasks,group_tasks)

def genWeek(data):
    personal_tasks = data[0]
    group_tasks = data[1]
    week=[]
    day={"date","personal1","personal2","event1","event2"}
    for key in personal_tasks:
        day=[key.split(",")[1]]
        temp = []
        for elem in personal_tasks[key]:
            temp.append(elem.title)
        for i in range(0,3):
            if i < len(temp):
                day.append(temp[i])
            else:
                day.append("")
        week.append(day)
    return week



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
        if not results:
            flash('No results found!')

    return render_template('search.html',
                           form=form,
                           query=form.search.data,
                           results=results)

## THIS IS NOT THE RIGHT STUFF RN, FROM LAST PROJ
@login_required
@app.route("/requests")
def requests():
    recieved = current_user().recieved_pending()
    counter = 0
    searchMatches = []
    try:
        for person in recieved:
            if(counter > 45):
                break
            info = []
            userDOB = current_user().dob.split("-")
            this = util.matchmaker.Person(userDOB[0], userDOB[1], userDOB[2])
            otherDOB = User.query_by_id(person, "dob").split("-")
            other = util.matchmaker.Person(otherDOB[0], otherDOB[1], otherDOB[2]) #Person object for other user
            other_user = User(person)
            info.append(other_user.name)
            info.append(round((util.matchmaker.personalityCompatibility(this, other))*100))
            info.append(round((util.matchmaker.sexualCompatibility(this, other))*100))
            info.append(round((util.matchmaker.inLawsCompatibility(this, other))*100))
            info.append(round((util.matchmaker.futureSuccess(this, other))*100))
            info.append(other_user.bio)
            info.append(person)
            info.append(round(current_user().user_dist(person)))
            info.append(other_user.get_starsign().capitalize())
            info.append(starsign_compatibilites[current_user().get_starsign()][other_user.get_starsign()])
            counter += 1
            searchMatches.append(info)
    except Exception as e:
        print(e)
    session["prev_url"]= "/requests/recieved"
    return render_template("requests.html", listings=searchMatches)

@login_required
@app.route('/myGroups', methods=['GET','POST'])
def myGroups():
    return render_template('mygroups.html',
                            groups = current_user.groups)

@login_required
@app.route('/leaveGroup', methods=['GET', 'POST'])
def leaveGroup():
    return "yo"

@login_required
@app.route('/addTask', methods=['GET','POST'])
def addTask():
    print(request.args)
    if 'title' in request.args.keys() and 'description' in request.args.keys() and 'date'in request.args.keys() and 'time' in request.args.keys():
        print("YOO")
        date = request.args['date'].split("/")
        month = int(date[0])
        day = int(date[1])
        if 'time' in request.args and request.args['time'] is not None:
            time = request.args['time'].split(":")
            hour = int(time[0])
            min = int(time[1])
        task = Task(current_user.id,month,day,hour,min,0,request.args['title'], request.args['description'])
        current_user.tasks.append(task)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('day'))

@login_required
@app.route('/addEvent', methods=['GET', 'POST'])
def addEvent():
    print(request.args)
    if 'title' in request.args.keys() and 'description' in request.args.keys() and 'date'in request.args.keys() and 'time' in request.args.keys():
        print("YOO")
        date = request.args['date'].split("/")
        time = request.args['time'].split(":")
        month = int(date[0])
        day = int(date[1])
        if 'time' in request.args:
            hour = int(time[0])
            min = int(time[1])
        task = Task(current_user.id,month,day,hour,min,0,request.args['title'],request.args['description'])
        current_user.tasks.append(task)
        db.session.add(task)
        db.session.commit()
    return redirect(url_for('day'))

@login_required
@app.route('/joinGroup/<group_id>', methods=['POST'])
def joinGroup(group_id):
    group = Group.query.filter_by(id = group_id).first()
    current_user.groups.append(group)
    db.session.commit()
    flash('You\'ve successfully joined the group!','success')
    return redirect(url_for('search'))

@login_required
@app.route('/createGroup', methods=['POST'])
def createGroup():
    print(request.form.keys())
    if 'name' in request.form.keys() and 'description' in request.form.keys() and 'private' in request.form.keys():
        print("YOOO")
        group = Group(request.form['name'], current_user.id, request.form['description'], request.form['private'])
        current_user.groups.append(group)
        db.session.add(group)
        db.session.commit()
    # if 'group name' in title.args.keys():
    #     Group.query.filter_by(id = 2)
    return redirect(url_for('search'))

@login_required
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/deleteTask', methods=['GET', 'POST'])
def deleteTask():
    return "f"
@app.route('/editTask', methods=['GET', 'POST'])
def editTask():
    return "f"
@app.route('/editGroup', methods=['GET', 'POST'])
def editGroup():
    return "f"

if __name__ == "__main__":
    app.debug = True
    app.run()
