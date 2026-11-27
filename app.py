import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import Config
from models import User, db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = "login"


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Import routes after app initialization to avoid a circular import.
from routes import *  # noqa: E402,F401,F403


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
