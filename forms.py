from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    name=StringField("Name",validators=[DataRequired()])
    email=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    register=SubmitField("REGISTER")


# TODO: Create a LoginForm to login existing users

class LoginForm(FlaskForm):
    email=StringField("Email",validators=[DataRequired()])
    password=PasswordField("Password",validators=[DataRequired()])
    submit=SubmitField("Log In")
# TODO: Create a CommentForm so users can leave comments below posts
class Submitdata(FlaskForm):
    user_data=StringField("UserName")
    user_dob=StringField("Date")
