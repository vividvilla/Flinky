from flinky import db
from urlparse import urlparse
from utils import make_pw_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique = True)
    email = db.Column(db.String(80), unique = True)
    password = db.Column(db.Text)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = make_pw_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)        

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