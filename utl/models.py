from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
from datetime import datetime

db = SQLAlchemy()

class GroupLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    credibility = db.Column(db.Integer)

    user = db.relationship('User', backref='groupownership')
    group = db.relationship('Group', backref='groupownership')

    def __init__(self, user_id, group_id):
        self.user_id = user_id
        self.group_id = group_id

class User(db.Model, UserMixin):
    # columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    tasks = db.relationship('Task', backref='user')
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
    tasks = db.relationship('Task', backref='group')
    users = association_proxy('groupownership',
                              'user',
                              creator=lambda u: GroupLinks(u.id, id))
    def __init__(self, name):
        self.name = name

class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

    due_date = db.Column(db.DateTime, nullable = False)
    priority = db.Column(db.Integer, nullable = False)
    timestamp = db.Column(db.DateTime, nullable=False,
                                       default=datetime.utcnow)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    upvotes = db.Columnn(db.Integer, nullable = False)
    downvotes = db.Column(db.Integer, nullable = False)


    def __init__(self, due_date, priority, title, description):
        self.due_date = due_date
        self.priority = priority
        self.title = title
        self.description = description
        self.upvotes = 0
        self.downvotes = 0
