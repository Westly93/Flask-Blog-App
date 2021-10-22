from flask_wtf import FlaskForm
from flaskblog.models import Post
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# Create the add post form
class UserCreatePostForm(FlaskForm):
    title= StringField('Title', validators= [DataRequired()])
    content= TextAreaField('Content', validators= [DataRequired()])
    submit= SubmitField('Post')
