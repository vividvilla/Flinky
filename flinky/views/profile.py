from flinky import app, user_loggedin, requires_login
from flask import render_template, session, url_for, redirect, request
from ..forms import ProfileForm
from ..models import db, User
from datetime import datetime
from ..utils import make_pw_hash

def calc_joined(joined_date):
	curr_date = datetime.now()
	seconds = (curr_date - joined_date).seconds
	days = (curr_date - joined_date).days
	if days > 365:
		return "{} years".format(days/365)
	elif days > 30:
		return "{} months".format(days/30)
	elif days > 0:
		return "{} days".format(days)
	elif seconds > 3600:
		return "{} hours".format(seconds/3600)
	elif seconds > 60:
		return "{} minutes".format(seconds/60)
	else:
		return "{} seconds".format(seconds)

@app.route('/profile/')
@app.route('/profile/<username>/')
@requires_login
def profile(username = None):
	if username:
		user = User.query.filter_by(username = username).first()
		return render_template('profile.html', user = user, joined = calc_joined(user.joined))
	return redirect('/')

@app.route('/profile/edit/<username>/', methods = ['GET', 'POST'])
@requires_login
def profile_edit(username):
	form = ProfileForm()
	user = User.query.filter_by(username = username).first()
	if form.validate_on_submit():
		password = form.password.data
		if password:
			user.password = make_pw_hash(password)
		
		email = form.email.data
		if email:
			user.email = email

		db.session.commit()
		return redirect(url_for('profile', username = username))
	return render_template('profile-edit.html', user = user, form = form)