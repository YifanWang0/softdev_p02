from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class GroupLinks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))

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

    def __init__(self, id, name):
        self.id = id
        self.name = name
