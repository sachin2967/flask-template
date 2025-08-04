from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlsplit

# Import the 'app' and 'db' objects that are created in app.py
from app import app, db
# Import the models and forms
from models import User, Project
from forms import LoginForm, RegistrationForm, ProjectForm


@app.route('/')
@app.route('/index')
def index():
    projects = Project.query.all()
    return render_template('index.html', title='Home', projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('admin')
        return redirect(next_page)
        
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/admin')
@login_required
def admin():
    projects = Project.query.all()
    return render_template('admin.html', title='Admin Panel', projects=projects)

@app.route('/add_project', methods=['GET', 'POST'])
@login_required
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            image_url=form.image_url.data,
            project_link=form.project_link.data,
            tags=form.tags.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Your project has been added!', 'success')
        return redirect(url_for('admin'))
    return render_template('add_edit_project.html', title='Add Project', form=form)

@app.route('/edit_project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    form = ProjectForm()
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.image_url = form.image_url.data
        project.project_link = form.project_link.data
        project.tags = form.tags.data
        db.session.commit()
        flash('Your project has been updated!', 'success')
        return redirect(url_for('admin'))
    elif request.method == 'GET':
        form.title.data = project.title
        form.description.data = project.description
        form.image_url.data = project.image_url
        form.project_link.data = project.project_link
        form.tags.data = project.tags
    return render_template('add_edit_project.html', title='Edit Project', form=form)

@app.route('/delete_project/<int:project_id>', methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Your project has been deleted.', 'success')
    return redirect(url_for('admin'))