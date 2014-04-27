from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL
from models import user_validation, email_validation, link_validation

def make_optional(field):
    field.validators.insert(0, Optional())

class LoginForm(Form):
	username = StringField('Username', validators = [DataRequired(message = "Username should not be empty")])
	password = PasswordField('Password', validators = [DataRequired(message = "Password should not be empty")])
	remember = BooleanField('remember', default = False)

class SignupForm(Form):
	username = StringField('Desired Username', validators = [DataRequired(), 
		Length(min=3,max=24, message = "Length must be around 3-20 letters"), user_validation])
	password = PasswordField('Password', validators = [DataRequired(),
		Length(min=5,max=80,message = "Password should be of atleast 5 letters")])
	confirm = PasswordField('Confirm Password', validators = [DataRequired(),
		EqualTo('password', message="Passwords doesn't match")])
	email = StringField('Email id', validators = [DataRequired(), Email(message="Invalid email id"), email_validation])

class ProfileForm(Form):
	password = PasswordField('New Password', validators = [Optional()])
	confirm = PasswordField('Confirm Password', validators = [EqualTo('password', message="Passwords doesn't match")])
	email = StringField('Email id', validators = [Email(message="Invalid email id"), email_validation, Optional()])

class LinkForm(Form):
	link = StringField('Link', validators = [DataRequired(), URL(message="Enter a valid URL"), link_validation])
	title = StringField('Title', validators = [Length(min=10,max=140, message = "Title must be 10-140 characters long"), Optional()])