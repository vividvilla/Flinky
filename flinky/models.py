from flinky import app
from urlparse import urlparse
from utils import make_pw_hash
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms.validators import ValidationError

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(80), unique = True)
    password = db.Column(db.Text)
    joined = db.Column(db.DateTime())

    def __init__(self, username, password, email, joined = datetime.now()):
        self.username = username
        self.email = email
        self.password = make_pw_hash(password)
        self.joined = joined

    def __repr__(self):
        return '<User %r>' % self.username

class Link(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String(240), unique = True)
    points = db.Column(db.Integer)
    domain = db.Column(db.String(240))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref = 'link', uselist=False)

    def __init__(self, link, user, points = 0, domain = ""):
        self.link = link
        self.user = user
        self.points = points

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