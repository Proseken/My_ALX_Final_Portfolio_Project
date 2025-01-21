from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo

#Registration Form
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(),Length(min=3,max=20)])
    email = StringField('email', validators=[DataRequired(),Email()])
    password = PasswordField('password', validators=[DataRequired(),Length(min=6,max=16)])
    confirm_password= PasswordField('confirm password', validators=[DataRequired(),EqualTo('password')])
    submit=SubmitField('Sign up')

#Login Form
class LoginForm(FlaskForm):
    email = StringField(label='email', validators=[DataRequired(),Email()])
    password = PasswordField(label='Password', validators=[DataRequired(),Length(min=6,max=16)])
    submit=SubmitField(label='Login')

