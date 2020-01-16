
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

db = SQLAlchemy()

class GroupLinks(db.Model): #this is automatically created when you append users to groups or groups to users
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    credibility = db.Column(db.Integer, nullable = False)

    user = db.relationship('User', backref='groupownership')
    group = db.relationship('Group', backref='groupownership')

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id
        self. credibility = 100

class User(db.Model, UserMixin):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    #relationships
    tasks = db.relationship('Task', backref='user') #whenever you create a task, append it to user.tasks
    admin_groups = db.relationship('Group', backref='user') #whenever you create a group, append it to the users admin groups who created it
    groups = association_proxy('groupownership', #whenever a user joins a group, append it to their groups
                              'group',
                              creator=lambda c: GroupLinks(id, c.id))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Group(db.Model):
    # columns`
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), nullable=False)
    private = db.Column(db.Boolean)
    #relationships
    tasks = db.relationship('Task', backref='group')
    users = association_proxy('groupownership',
                              'user',
                              creator=lambda u: GroupLinks(u.id, id))
    def __init__(self, name, user_id, description, private):
        self.name = name
        self.description = description
        self.admin_id = user_id
        self.private = private

class Task(db.Model):
    #columns
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable = False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    due_date_m = db.Column(db.Integer, nullable = False)
    due_date_d = db.Column(db.Integer, nullable = False)
    due_date_hr = db.Column(db.Integer)
    due_date_mm = db.Column(db.Integer)
    priority = db.Column(db.Integer, nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False,
                                       default=datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)

    def __init__(self, user_id, month, day, hour, min, priority, title, description):
        self.user_id = user_id
        self.due_date_m = month
        self.due_date_d = day
        self.due_date_hr = hour
        self.due_date_mm = min
        self.priority = priority
        self.title = title
        self.description = description
        self.upvotes = None
        self.downvotes = None
