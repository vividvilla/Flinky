from os import urandom
from binascii import b2a_hex
import hashlib
import requests
import re
from datetime import datetime

from flinky import app

SECRET = app.config['SECRET_KEY']

def random_pass(num):
	return b2a_hex(urandom(num))

def make_pw_hash(pw, name=SECRET, salt=""):
    if salt == "":
        salt = random_pass(15)
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_password(pw, h, name=SECRET):
    salt = h.split('|')[1]
    if make_pw_hash(pw, name, salt) == h:
        return True

def get_title(url):
	r = requests.get(url).text
	titlecomp = re.compile("<title>(.+?)</title>", re.IGNORECASE|re.DOTALL)
	title = titlecomp.search(r)
	if title:
		return title.group(1).strip()
	return "No title"

def calc_time(date):
	curr_date = datetime.now()
	diff = curr_date - date
	seconds = diff.seconds
	days = diff.days
	if days > 365:
		return "{} years".format(days/365)
	elif days > 30:
		return "{} months".format(days/30)
	elif days > 1:
		return "{} days".format(days)
	elif seconds > 7200:
		return "{} hours".format(seconds/3600)
	elif seconds > 120:
		return "{} minutes".format(seconds/60)
	else:
		return "{} seconds".format(seconds)