from app import app, db
from app.models import Users, Classs, Students, Enrolment, StudentData
from flask import render_template, flash, redirect, request, url_for, session
from app.forms import SignupForm, LoginForm, ClassForm, EnrolForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind = engine)
session = Session()

@app.route('/signup', methods=['GET', 'POST'])
def Signup():
    form = SignupForm()

    if form.validate_on_submit():

        user = Users()
        user.username = form.username.data;
        user.password = form.password.data;
        user.useremail = form.email.data;

        db.session.add(user)
        db.session.commit()
        

        flash('Login requested for user{}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/login')
    return render_template('signup.html', title='Sign Up', form=form)



@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username_or_email.data).first()
        if user is None or not Users.query.filter_by(password=form.password.data).first():
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user', username=current_user.username))

    return render_template('login.html', title='Login', form=form)
        

@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/enrol", methods=['GET', 'POST'])
def enrol():

    form = EnrolForm()

    if form.validate_on_submit():
        student = Students()
        

        student.studentname = form.studentname.data;
        student.studentcode = form.studentcode.data;

        db.session.add(student)
        db.session.commit()

        # creating enrolment
        enrolment = Classs.query.filter_by(classcode = form.classcode.data).first()

        student.classes.append(enrolment)
        
        #commiting enrolment

        db.session.add(student)
        db.session.commit()

        print("got here")




    return render_template('enrolment.html', form=form)


def StudentsInClass(classs):

    
    dict_structure = {
        "classcode": "",
        "students": []
    }   

    class_length = len(classs);

    dicts = []

    for i in range(class_length):
        newdict = dict_structure
        newdict["classcode"] = classs[i].classcode
        newdict["students"] = classs[i].students
        dicts.append(newdict)
    
    return dicts;
    



@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    #Only allow users to see their users page
    form = ClassForm();
    user = Users.query.filter_by(username=username).first_or_404()
    if(current_user.get_id() == user.get_id()):
        

        classs = Classs.query.filter_by(teacherid = int(current_user.get_id())).all()
        #testClass = Classs.query.filter_by(classcode = "jacob").first()

        
        dicts = StudentsInClass(classs);
        #print(dicts[0]["students"][0])

        

        print()

        if form.validate_on_submit():
            thisClass = Classs();
            thisClass.teacherid = int(current_user.get_id());
            thisClass.classcode = form.class_code.data;

            db.session.add(thisClass)
            db.session.commit()
        
        return render_template('user.html', user=user, form=form, classes=classs, dicts=dicts)  
    else:

        return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')