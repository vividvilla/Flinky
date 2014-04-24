import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flinky.db')
SECRET_KEY = 'SOMERANDOMSECRETKEY'
WTF_CSRF_SECRET_KEY = 'SOMERANDOMSECRETKEY'
WTF_CSRF_ENABLED = True