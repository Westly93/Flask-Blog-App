from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from flaskblog.models import User




class UserRegistrationForm(FlaskForm):
    username= StringField('Username', validators= [DataRequired(), Length(min= 2, max= 20)])
    email= StringField('Email', validators= [DataRequired(), Email()])
    password= PasswordField('Password', validators= [DataRequired()])
    confirm_password= PasswordField('Confirm Password', validators= [DataRequired(), EqualTo('password')])
    submit= SubmitField('Sign Up')

    #def validate_field(self, field):
    #    if True:
    #        return ValidationError('Validation Message')

    def validate_username(self, username):
        user= User.query.filter_by(username= username.data).first()
        if user:
            raise ValidationError('This username is taken. Please choose different one!')

    def validate_email(self, email):
        user= User.query.filter_by(email= email.data).first()
        if user:
            raise ValidationError('This email is taken. Please choose a different one!')

class UserLoginForm(FlaskForm):
    email= StringField('Email', validators= [DataRequired(), Email()])
    password= PasswordField('Password', validators= [DataRequired()])
    remember= BooleanField('Remember me')
    submit= SubmitField('login')

class UserUpdateAccountForm(FlaskForm):
    username= StringField('Username', validators= [DataRequired(), Length(min= 2, max= 20)])
    email= StringField('Email', validators= [DataRequired(), Email()])
    picture= FileField('Update profile picture', validators= [FileAllowed(['jpg', 'png'])])
    submit= SubmitField('Update')

    def validate_username(self, username):
        if username.data!= current_user.username:
            user= User.query.filter_by(username= username.data).first()
            if user:
                raise ValidationError('This username is taken. Please Choose a different one')

    def validate_email(self, email):
        if email.data!= current_user.email:
            user= User.query.filter_by(email= email.data).first()
            if user:
                raise ValidationError('This email is taken. Please choose a different one')


class RequestResetForm(FlaskForm):
    email= StringField('Email', validators= [DataRequired(), Email()])
    submit= SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email= email.data)
        if user is None:
            raise ValidationError('There is no account with that email. You need to register')

class ResetPasswordForm(FlaskForm):
    password= PasswordField('Old Password', validators= [DataRequired()])
    confirm_password= PasswordField('New Password', validators= [DataRequired(), EqualTo('password')])
    submit= SubmitField('Password Reset')
