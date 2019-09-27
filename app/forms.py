from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email
from app.models import Users



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    useremail = StringField('Email', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

    
    
    def validate_username(self, username):
        user_unique_test = Users.query.filter_by(username = username.data).first()
        if user_unique_test is not None:
            raise ValidationError('test')

    def validate_email(self, useremail):
        email_unique_test = Users.query.filter_by(useremail = useremail.data).first()
        if email_unique_test is not None:
            raise ValidationError('test2')



class LoginForm(FlaskForm):
    username_or_email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class ClassForm(FlaskForm):
    class_code = StringField('code', validators=[DataRequired()])
    submit = SubmitField('Create Class')


class EnrolForm(FlaskForm):
    studentname = StringField('studentname', validators=[DataRequired()])
    studentcode = IntegerField('studentcode', validators=[DataRequired()])
    classcode = StringField('classcode', validators=[DataRequired()])
    submit = SubmitField('Enrol')


class UserEditForm(FlaskForm):
    classname = StringField('classname', validators=[DataRequired()])
    newclassname = StringField('newclassname', validators=[DataRequired()])
    submit = SubmitField('Change Classname')




