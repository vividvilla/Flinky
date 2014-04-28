from flinky import app, user_loggedin, requires_login
from flask import render_template, session, url_for, redirect, request, flash
from ..forms import LinkForm
from ..models import db, User, Link
from sqlalchemy import desc

@app.route('/')
def index():
	links = Link.query.order_by(desc(Link.id)).all()
	return render_template('home.html', links = links)

@app.route('/submit/', methods = ['GET', 'POST'])
@requires_login
def submit():
	form = LinkForm()
	if form.validate_on_submit():
		link = form.link.data
		title = form.title.data
		user = User.query.filter_by(username = session['logged_in']).first()
		new_link = Link(link,user,title)
		db.session.add(new_link)
		db.session.commit()
		flash("Link successfully submitted", category = 'success')
		return redirect('/')
	return render_template('submit.html', form = form)

@app.route('/link/delete/<linkid>/')
@requires_login
def delete_link(linkid):
	next_url = request.args.get('prev')
	link = Link.query.filter_by(id = linkid).first()
	if link.user.username == session['logged_in']:
		db.session.delete(link)
		db.session.commit()
		flash("Link deleted", category = "success")
		return redirect(next_url)
	flash("You are not allowed this action", category = "error")
	return redirect('/')

@app.route('/link/upvote/<linkid>/')
@requires_login
def upvote(linkid):
	next_url = request.args.get('prev')
	user = User.query.filter_by(username = session['logged_in']).first()
	link = Link.query.filter_by(id = linkid).first()
	if link.user.id == user.id:
		flash('You cannot upvote your own link', category= "error")
		return redirect(next_url)
	if user in link.upvotes:
		link.upvotes.remove(user)
		link.points = link.points - 1
		link.user.karma = link.user.karma - 1
		db.session.commit()
		flash("Your vote removed", category = "success")
		return redirect(next_url)
	link.upvotes.append(user)
	link.points = link.points + 1
	link.user.karma = link.user.karma + 1
	db.session.commit()
	flash("Successfully upvoted", category = "success")
	return redirect(next_url)

@app.template_filter('submitted_by_me')
def submitted_by_me(upvotes):
	user = User.query.filter_by(username = session['logged_in']).first()
	if user in upvotes:
		return "submitted-by-me"