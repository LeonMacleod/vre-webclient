from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email
from app.models import Users, Classs



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')


    #Validation helper function, used to prevent users being created of the same username.
 
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

    #Validation helper function, used to prevent classes being created with the same classcode.

    def validate_class_code(self, class_code):
        class_code_unique_test = Classs.query.filter_by(classcode = class_code.data).first()
        if class_code_unique_test is not None:
            raise ValidationError('This class code is already in use.')


class StudentHelper(FlaskForm):
    studentid = IntegerField('studentid', validators=[DataRequired()])
    gameid = IntegerField('gameid', validators=[DataRequired()])
    score = IntegerField('score', validators=[DataRequired()])
    areamost = StringField('areamost', validators=[DataRequired()])
    arealeast = StringField('arealeast', validators=[DataRequired()])
    improvementrate = StringField('improvementrate', validators=[DataRequired()])
    studentname = StringField('studentname', validators=[DataRequired()])
    classid = IntegerField('classid', validators=[DataRequired()])

    submit = SubmitField('Insert Student Data')
    
class EnrolForm(FlaskForm):
    studentname = StringField('studentname', validators=[DataRequired()])
    studentcode = IntegerField('studentcode', validators=[DataRequired()])
    classcode = StringField('classcode', validators=[DataRequired()])
    submit = SubmitField('Enrol')


class UserEditForm(FlaskForm):
    classname = StringField('classname', validators=[DataRequired()])
    newclassname = StringField('newclassname', validators=[DataRequired()])
    submit = SubmitField('Change Classname')



