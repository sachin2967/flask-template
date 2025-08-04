from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, URL, Optional
from models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Optional(), URL(
        message="Invalid URL.")], render_kw={"placeholder": "https://example.com/image.png"})
    project_link = StringField('Project Link', validators=[Optional(), URL(
        message="Invalid URL.")], render_kw={"placeholder": "https://github.com/user/repo"})
    tags = StringField('Tags (comma-separated)',
                       render_kw={"placeholder": "Python, Flask, Data Science"})
    submit = SubmitField('Submit Project')
