# Flask Portfolio Starter

A small server-rendered portfolio/content-management starter built with Flask. It demonstrates form handling, user registration and login, SQLAlchemy models, database migrations, and authenticated project CRUD pages.

> **Status and security boundary:** This is a learning/starter application, not a production-ready multi-user CMS. The current routes protect the project-management pages with login checks but do not implement role-based administrator authorization: any registered user can reach those pages. Add an explicit administrator model and authorization policy before deploying it publicly.

## Features

- Flask application with Jinja templates
- Registration, login, logout, password hashing and session management through Flask-Login
- Project records with title, description, image URL, project link and tags
- Create, edit and delete project routes
- SQLAlchemy persistence with Flask-Migrate
- Environment-based secret and database configuration

## Tech stack

- Python and Flask
- Flask-Login, Flask-WTF and Flask-Migrate
- Flask-SQLAlchemy / SQLAlchemy
- SQLite for local development; another SQLAlchemy-supported database can be configured through `DATABASE_URL`

## Local setup

Requires Python and a version compatible with the packages in `requirements.txt`.

```bash
git clone https://github.com/sachin2967/flask-template.git
cd flask-template

python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"
```

Put the generated value in `.env` as `SECRET_KEY`. On Windows, copy `.env.example` to `.env` manually if `cp` is unavailable. The real `.env` file is ignored by Git; do not commit it.

Initialize the migration repository once, then create and apply the initial schema:

```bash
flask --app app db init
flask --app app db migrate -m "Initial schema"
flask --app app db upgrade
flask --app app run
```

The app is available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

For local debugging only, set `FLASK_DEBUG=1` in `.env`. Debug mode is off by default.

## Configuration

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Required signing key for Flask sessions and related security features |
| `DATABASE_URL` | Optional SQLAlchemy database URL; defaults to local SQLite |
| `FLASK_DEBUG` | Set to `1` only for local development |

## Main routes

| Route | Purpose |
| --- | --- |
| `/`, `/index` | Public project listing |
| `/register` | Create an account |
| `/login`, `/logout` | Session authentication |
| `/admin` | Authenticated project list |
| `/add_project` | Create a project |
| `/edit_project/<id>` | Update a project |
| `/delete_project/<id>` | Delete a project (POST) |

## Before any public deployment

This repository is intentionally a starter. At minimum, implement role-based authorization (the present login check is not an admin role), restrict or disable open registration, configure HTTPS and secure cookie settings, add request rate limits and security headers, review CSRF and upload handling, use managed secrets, and establish database backups and migrations. Do not reuse example credentials or expose a development server to the internet.

## Repository structure

```text
app.py          Flask app and extension initialization
config.py       Environment-backed application configuration
models.py       SQLAlchemy models
forms.py        WTForms definitions
routes.py       Authentication and project CRUD routes
templates/      Jinja page templates
requirements.txt
.env.example    Safe configuration template
```

## License

No license is currently specified. All rights remain with the copyright holder unless a license is added.
