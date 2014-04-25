from flinky import app, user_loggedin, requires_login
from flask import render_template, session, url_for, redirect, request
from ..forms import LoginForm, SignupForm
from ..models import db, User
from ..utils import valid_password

@app.route('/login/', methods = ('GET', 'POST'))
@user_loggedin
def login():
	form = LoginForm()
	if form.validate_on_submit():
		password = form.password.data
		username = form.username.data
		user = User.query.filter_by(username = username).first()
		if user:
			if valid_password(password, user.password):
				session['logged_in'] = user.username
				session.permanent = form.remember.data
				return redirect('/')
	return render_template('login.html', form = form)

@app.route('/signup/', methods = ('GET','POST'))
@user_loggedin
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		email = form.email.data
		new_user = User(username, password, email)
		db.session.add(new_user)
		db.session.commit()
		session['logged_in'] = new_user.username
		return "Hello {}".format(new_user.username)
	return render_template('signup.html', form = form)

@app.route('/logout/')
@requires_login
def logout():
    if session.get('logged_in'):
        session.pop('logged_in', None)
    return redirect('/')