import os

DEBUG = True
SECRET_KEY = 'my precious'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#HOST = 'localhost'
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5000))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.db')
