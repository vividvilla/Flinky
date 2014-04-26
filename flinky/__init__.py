from flask import Flask, session, redirect, url_for, request, flash
from functools import wraps

app = Flask(__name__)
app.config.from_object('config')

@app.before_request
def set_session():
    session.modified = True

def requires_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("You need to either login or signup to access this page", category = "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def user_loggedin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('logged_in'):
            return redirect(url_for('profile', username = session['logged_in']))
        return f(*args, **kwargs)
    return decorated_function

# @app.route('/')
# @requires_login
# @user_loggedin
# def index():
#     return None

import flinky.views