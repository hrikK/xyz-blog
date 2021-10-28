from app.models import user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.fields.html5 import TelField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import Length, DataRequired, Email, EqualTo, ValidationError

class msgForm(FlaskForm):
    name = StringField(label="Name", validators=[Length(min=3, max=18), DataRequired()])
    email = StringField(label="Email address", validators=[Email(), DataRequired()])
    phone = TelField(label="Phone Number", validators=[DataRequired()])
    message = TextAreaField(label="Message", validators=[DataRequired()])
    submit = SubmitField(label="SEND")

class SignUpForm(FlaskForm):
    def validate_username(self, username_to_check):
        username_check = user.query.filter_by(username=username_to_check.data).first()
        if username_check:
            raise ValidationError("Username is already been used!")

    def validate_email(self, email_to_check):
        email_check = user.query.filter_by(email=email_to_check.data).first()
        if email_check:
            raise ValidationError("Email is already registered!")
    
    name = StringField(label="Name", validators=[Length(min=3, max=20), DataRequired()])
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    username = StringField(label="Username", validators=[Length(min=3, max=8), DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label="Join Now")

class ImageForm(FlaskForm):
    img = FileField(label="Select Image", validators=[FileAllowed(["png", "jpg", "jpeg"]), FileRequired()])
    submit = SubmitField(label="Upload Picture")

class SignInForm(FlaskForm):
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log In")

class PostForm(FlaskForm):
    title = StringField(label="Title", validators=[Length(min=8, max=50), DataRequired()])
    subtitle = StringField(label="Subtitle", validators=[Length(min=10, max=80), DataRequired()])
    body = TextAreaField(label="Body", validators=[DataRequired()])
    post_bg = FileField(label="Upload background for your blog", validators=[FileAllowed(["png", "jpg", "jpeg"]), FileRequired()])
    publish = SubmitField(label="Publish Post")
    save = SubmitField(label="Save Post")