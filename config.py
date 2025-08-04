# In config.py
import os
from dotenv import load_dotenv

# Find the absolute path of the directory containing this file
basedir = os.path.abspath(os.path.dirname(__file__))
# Load environment variables from .env
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    # A secret key is needed for security (e.g., for signing session cookies)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fsildjflsdjflsjfjdfs'

    # This sets up the database URI. It will use the DATABASE_URL from Heroku if it exists,
    # otherwise, it will create a local SQLite database named 'app.db'.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # This is just to suppress a warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False
