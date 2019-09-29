from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email
from app.models import Users, Classs



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')
 
    def validate_username(self, username):
        user_unique_test = Users.query.filter_by(username = username.data).first()
        if user_unique_test is not None:
            raise ValidationError('This username is already taken!')


class LoginForm(FlaskForm):
    username_or_email = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class ClassForm(FlaskForm):
    class_code = StringField('code', validators=[DataRequired()])
    submit = SubmitField('Create Class')

    def validate_class_exists(self, provided_classcode):
        classs = Classs.query.filter_by(classcode = provided_classcode.data).first()
        if classs is None:
            raise ValidationError('This class does not exist!')


class EnrolForm(FlaskForm):
    studentname = StringField('studentname', validators=[DataRequired()])
    studentcode = IntegerField('studentcode', validators=[DataRequired()])
    classcode = StringField('classcode', validators=[DataRequired()])
    submit = SubmitField('Enrol')


class UserEditForm(FlaskForm):
    classname = StringField('classname', validators=[DataRequired()])
    newclassname = StringField('newclassname', validators=[DataRequired()])
    submit = SubmitField('Change Classname')




