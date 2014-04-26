from flinky import app
from urlparse import urlparse
from utils import make_pw_hash, get_title
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms.validators import ValidationError

from flask import session

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(80), unique = True)
    password = db.Column(db.Text)
    joined = db.Column(db.DateTime())
    karma = db.Column(db.Integer(), default = 0)

    def __init__(self, username, password, email, joined = datetime.now(), karma = 0):
        self.username = username
        self.email = email
        self.password = make_pw_hash(password)
        self.joined = joined
        self.karma = karma

    def __repr__(self):
        return '<User %r>' % self.username

class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(240), unique = True)
    title = db.Column(db.String(240))
    points = db.Column(db.Integer)
    domain = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = 'link', uselist=False)

    def __init__(self, link, user, title = None, points = 0, domain = ""):
        self.link = link
        self.title = title
        self.user = user
        self.points = points

        if title:
            self.title = title
        else:
            self.title = get_title(link)

        parsed_uri = urlparse(link)
        self.domain =  '{uri.netloc}'.format(uri=parsed_uri)

    def __repr__(self):
        return '<Link %r>' % self.link

def user_validation(form, field):
    user = User.query.filter_by(username = field.data).first()
    if user:
        raise ValidationError('User already exists')

def email_validation(form, field):
    email = User.query.filter_by(email = field.data).first()
    if email:
        raise ValidationError('Emailid already registered')

def link_validation(form, field):
    link = Link.query.filter_by(link = field.data).first()
    if link:
        raise ValidationError('This link is already submitted')