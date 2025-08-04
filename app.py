from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from models import db

# Create an instance of the Flask application.
app = Flask(__name__)
# Load the configuration settings from the Config class.
app.config.from_object(Config)

# Initialize extensions with our app
db.init_app(app)
migrate = Migrate(app, db)
login = LoginManager(app)
# Tell Flask-Login which page to redirect to for users who are not logged in.
login.login_view = 'login'

# Import the User model for the user_loader
from models import User

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Import the routes from routes.py
# This is placed at the bottom to avoid a "circular import" error,
# because routes.py needs to import the 'app' variable defined above.
from routes import *

if __name__ == '__main__':
    app.run(debug=True)