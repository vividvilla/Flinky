from flinky import app, user_loggedin, requires_login
from flask import render_template, session, url_for, redirect, request, flash
from ..forms import LinkForm
from ..models import db, User, Link

@app.route('/')
def index():
	links = Link.query.all()
	return render_template('home.html', links = links)