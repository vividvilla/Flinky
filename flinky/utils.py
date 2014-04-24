from os import urandom
from binascii import b2a_hex
import hashlib

from flinky import app

SECRET = app.config['SECRET_KEY']

def random_pass(num):
	return b2a_hex(urandom(num))

def make_pw_hash(pw, name=SECRET, salt=""):
    if salt == "":
        salt = random_pass(15)
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (h, salt)

def valid_pw(pw, h, name=SECRET):
    salt = h.split('|')[1]
    if make_pw_hash(pw, name, salt) == h:
        return True