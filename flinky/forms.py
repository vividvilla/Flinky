from flask_wtf import Form
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(Form):
	username = StringField('username', size=30, maxlength=50, validators = [DataRequired(message = "Username should not be empty")])
	password = PasswordField('password', validators = [DataRequired(message = "Password should not be empty")])
	remember = BooleanField('remember', default = False)

class SignupForm(Form):
	username = StringField('username', validators = [DataRequired(), 
		Length(min=3,max=24, message = "Length must be around 3-20 letters")])
	password = PasswordField('password', validators = [DataRequired(),
		Length(min=5,max=80,message = "Password should be of atleast 5 letters")])
	confirm = PasswordField('confirm', validators = [DataRequired(),
		EqualTo('password', message="Passwords must match")])
	email = StringField('email', validators = [DataRequired(),
		Email(message="Invalid email id")])