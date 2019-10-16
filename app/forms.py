from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, Length
from app.models import Users, Classs


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


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')


    #Validation helper function, used to prevent users being created of the same username.
 
    def validate_username(self, username):
        user_unique_test = Users.query.filter_by(username = username.data).first()
        if user_unique_test is not None:
            raise ValidationError('This username is already taken!')


class LoginForm(FlaskForm):
    username_or_email = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=50)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class ClassForm(FlaskForm):
    class_code = StringField('code', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Create Class')

    #Validation helper function, used to prevent classes being created with the same classcode.

    def validate_class_code(self, class_code):
        class_code_unique_test = Classs.query.filter_by(classcode = class_code.data).first()
        if class_code_unique_test is not None:
            raise ValidationError('This class code is already in use.')



    
class EnrolForm(FlaskForm):
    studentname = StringField('studentname', validators=[DataRequired(), Length(max=20)])
    studentcode = StringField('studentcode', validators=[DataRequired(), Length(max=50)])
    classcode = StringField('classcode', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Enrol')


class UserEditForm(FlaskForm):
    classname = StringField('classname', validators=[DataRequired()])
    newclassname = StringField('newclassname', validators=[DataRequired()])
    submit = SubmitField('Change Classname')



