import os

# grabs the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'umotasks.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = '6&xdc9x14xee>x9b&&xbdx9@8xdbFSjx8#x7fx9bxb3x89xe4x8dxf&&exa4x10x1axe8'

# defines the full path for the database
DATABASE_PATH = os.path.join(basedir, DATABASE)
