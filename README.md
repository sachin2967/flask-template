## Project Structure

```
/flask_portfolio_template
├── venv/                 # The locally generated virtual environment (Ignored by Git)
├── migrations/
├── static/
├── templates/
├── .env
├── .gitignore
├── app.py
├── config.py
├── forms.py
├── models.py
├── Procfile
├── README.md
├── requirements.txt
└── routes.py
```

## Local Setup & Run Commands (Windows)

**1. Clone Repository**

```cmd
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

**2. Create and Activate Virtual Environment**

```cmd
python -m venv venv
venv\Scripts\activate
```

**3. Install Dependencies**

```cmd
pip install -r requirements.txt
```

**4. Create Environment File**
Create a new file named `.env` in the root project folder and add this line:

```
SECRET_KEY='my-local-dev-secret-key'
```

**5. Initialize Database**

```cmd
set FLASK_APP=app.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

_(Note: `flask db init` is only needed once per project.)_

**6. Run the Local Server**

```cmd
flask run
```

The application will be available at `http://127.0.0.1:5000`.

---

## Deployment to Heroku (Windows)

**1. Create `requirements.txt` File**

```cmd
pip freeze > requirements.txt
```

**2. Create `Procfile`**
Create a file named `Procfile` (no extension) in the root folder with this single line:

```
web: flask db upgrade; gunicorn app:app
```

**3. Deploy using Heroku CLI**

```cmd
heroku login
heroku create your-unique-app-name
heroku addons:create heroku-postgresql:hobby-dev
heroku config:set SECRET_KEY='$(openssl rand -base64 32)'
git push heroku main
heroku open
```
