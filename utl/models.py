from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

db = SQLAlchemy()

class GroupLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    admin = db.Column(db.Boolean, nullable = False)

    user = db.relationship('User', backref='groupownership')
    group = db.relationship('Group', backref='groupownership')

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id


class TaskLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))

    user = db.relationship('User', backref='taskownership')
    task = db.relationship('Task', backref='taskownership')

    def __init__(self, user_id, task_id):
        self.user_id = user_id
        self.group_id = task_id

class User(db.Model, UserMixin):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    groups = association_proxy('groupownership',
                              'group',
                              creator=lambda c: GroupLinks(id, c.id))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Group(db.Model):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = association_proxy('groupownership',
                              'user',
                              creator=lambda u: GroupLinks(u.id, id))
    def __init__(self, name):
        self.name = name

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    due_date = db.Column(db.DateTime, nullable = False)
    priority = db.Column(db.Integer, nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False,
                                       default=datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    upvotes = db.Columnn(db.Integer, nullable = False)
    downvotes = db.Column(db.Integer, nullable = False)

    users = association_proxy('taskownership',
                              'user',
                              creator=lambda u: GroupLinks(u.id, id))

    def __init__(self, due_date, priority, title, description):
        self.due_date = due_date
        self.priority = priority
        self.title = title
        self.description = description
        self.upvotes = 0
        self.downvotes = 0
