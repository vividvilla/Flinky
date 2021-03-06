from flinky import app, user_loggedin, requires_login
from flask import render_template, session, url_for, redirect, request, flash
from ..forms import LoginForm, SignupForm
from ..models import db, User
from ..utils import valid_password

@app.route('/login/', methods = ('GET', 'POST'))
@user_loggedin
def login():
	error = False
	form = LoginForm()
	if form.validate_on_submit():
		password = form.password.data
		username = form.username.data
		user = User.query.filter_by(username = username).first()
		if user:
			if valid_password(password, user.password):
				session['logged_in'] = user.username
				session.permanent = form.remember.data
				flash('You are loggedin', category = "success")
				return redirect('/')
			else:
				error = True
		else:
			error = True

	return render_template('login.html', form = form, error = error)

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
		flash('You are successfully registered', category = "success")
		return redirect('/profile')
	return render_template('signup.html', form = form)

@app.route('/logout/')
@requires_login
def logout():
    if session.get('logged_in'):
        session.pop('logged_in', None)
    flash('You are logged out', category = "success")
    return redirect('/')