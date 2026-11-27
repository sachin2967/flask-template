import os
from dotenv import load_dotenv

# Load local development configuration without overriding environment variables.
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    # Never fall back to a committed development secret.
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY is required. Copy .env.example to .env and set a random value."
        )

    # Use DATABASE_URL when provided; otherwise keep development data in SQLite.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or (
        "sqlite:///" + os.path.join(basedir, "app.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
