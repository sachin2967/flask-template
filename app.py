import os

import click

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
    return db.session.get(User, int(user_id))


# Import routes after app initialization to avoid a circular import.
from routes import *  # noqa: E402,F401,F403


@app.cli.command("grant-admin")
@click.argument("username")
def grant_admin(username):
    """Promote an existing account to administrator from a trusted shell."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise click.ClickException(f"No user found with username: {username}")
    if user.is_admin:
        click.echo(f"{username} is already an administrator.")
        return
    user.is_admin = True
    db.session.commit()
    click.echo(f"Granted administrator access to {username}.")


@app.cli.command("revoke-admin")
@click.argument("username")
def revoke_admin(username):
    """Remove administrator privileges from an existing account."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        raise click.ClickException(f"No user found with username: {username}")
    if not user.is_admin:
        click.echo(f"{username} is not an administrator.")
        return
    user.is_admin = False
    db.session.commit()
    click.echo(f"Revoked administrator access from {username}.")


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
