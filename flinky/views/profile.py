from flinky import app, user_loggedin, requires_login
from flask import render_template, session, url_for, redirect, request, flash
from ..forms import ProfileForm
from ..models import db, User, Link
from ..utils import make_pw_hash, calc_time

@app.route('/profile/')
@app.route('/profile/<username>/')
def profile(username = None):
	if username:
		user = User.query.filter_by(username = username).first()
		links = Link.query.filter_by(user = user).all()
		return render_template('profile.html', user = user, joined = calc_time(user.joined), links = links)

	if session.get('logged_in'):
		return redirect(url_for('profile', username = session['logged_in']))
	return redirect(url_for('login'))

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
		flash("Successfully modifed the profile", category = 'success')
		return redirect(url_for('profile', username = username))
	return render_template('profile-edit.html', user = user, form = form)