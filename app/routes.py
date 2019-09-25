from app import app, db
from app.models import Users, Classs, Students, Enrolment, StudentData
from flask import render_template, flash, redirect, request, url_for, session
from app.forms import SignupForm, LoginForm, ClassForm, EnrolForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_login import current_user, login_user, login_required, logout_user
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import json

#Route that handles page signup
@app.route('/signup', methods=['GET', 'POST'])
def Signup():

    # getting the WTFORM from the forms.py file.
    form = SignupForm()

    # Listening for form validation (what happens if someone clicks the submit button)
    if form.validate_on_submit():

        #creating a user instance
        user = Users()
        # setting its attributes from the form data.
        user.username = form.username.data;
        user.password = form.password.data;
        user.useremail = form.email.data;

        # adding and commiting the data to the database.
        db.session.add(user)
        db.session.commit()
        
        #feedback through flash
        flash('Login requested for user{}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/login')
    # rendering the template 'signup.html' on return parsing the variables title and form.
    return render_template('signup.html', title='Sign Up', form=form)


#Route that handles page login
@app.route('/login', methods=['GET', 'POST'])
def Login():
    # getting the WTFORM from the forms.py file.
    form = LoginForm()

    # if the user is already logged in we don't want them attempting to login again so they are redirected.
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    
    # if the login button is clicked.
    if form.validate_on_submit():
        # attempting to get a user in the database with the same username as that provided in the form
        user = Users.query.filter_by(username=form.username_or_email.data).first()
        #if this username provided does not correlate to a row in the database the user will be redirected.
        if user is None or not Users.query.filter_by(password=form.password.data).first():
            return redirect(url_for('Login'))
        #if this username provided does correlate to a row in the database the user is logged in and redirected to their user page.
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('user', username=current_user.username))
    # rendering the template 'login.html' on return parsing the variables Login and form.
    return render_template('login.html', title='Login', form=form)
        
# A simple route to logout the user.
@app.route("/logout", methods=['GET', 'POST'])
@login_required
def logout():
    #logs out the user
    logout_user()
    #redirects the user to the homepage
    return redirect(url_for('index'))

# The route for enrolment
@app.route("/enrol", methods=['GET', 'POST'])
def enrol():
    # Collecting the form from forms.py
    form = EnrolForm()

    # if the submit enrolment button is pressed
    if form.validate_on_submit():
        #creating a student instance
        student = Students()
        
        # setting the attributes of this instance to those specified in the form
        student.studentname = form.studentname.data;
        student.studentcode = form.studentcode.data;

        #adding and commiting to the session.
        db.session.add(student)
        db.session.commit()

        # creating enrolment
        enrolment = Classs.query.filter_by(classcode = form.classcode.data).first()

        # Creating the intermediate table between students and classes (enrolment) using the previously defined student instance (on enrolment)
        student.classes.append(enrolment)
        
        # adding and commiting enrolment
        db.session.add(student)
        db.session.commit()
    # on return the enrolment.html template is rendered and the form is parsed.
    return render_template('enrolment.html', form=form)

# Helper function for the user route, helps generate tables of classes directly
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
    

# Helper function for the user route, helps with with converting
# database data to python dictionaries to JSON strings to then have graphed data provided
# to the user.
def StudentDataHelper(data):

    dicts_to_return = []

    for i in(data):
        print("appendign at " + str(i.studentid))
        this_dict =  {
            "studentid": 0,
            "gameid": 0,
            "score": 0,
            "areamost": "",
            "arealeast": "",
            "improvementrate": 0,
            "studentname": "",
            "classid" : 0
        }
        this_dict["studentid"] = i.studentid
        this_dict["gameid"] = i.gameid
        this_dict["score"] = i.score
        this_dict["areamost"] = i.areamost
        this_dict["arealeast"] = i.arealeast
        this_dict["improvementrate"] = i.improvementrate
        this_dict["studentname"] = i.studentname
        this_dict["classid"] = i.classid
        dicts_to_return.append(this_dict)
    return dicts_to_return

# Route handling the users page
@app.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user(username):
    #Collecting form.
    form = ClassForm();
    
    #If the correct user is on this page the page will function as follows
    #If not the user will be redirected through render template to "index.html"
    user = Users.query.filter_by(username=username).first_or_404()
    if(current_user.get_id() == user.get_id()):
        
        # getting the classs data of the user (teacher) with the id of the current user(teacher)
        classs = Classs.query.filter_by(teacherid = int(current_user.get_id())).all()
        studentsinclass = []
        for i in range(len(classs)):
            #getting all students in this users class.
            studentsinclass.append(classs[i].students)


        studentdatapackets = []

        print(studentsinclass)
        print(len(studentsinclass))

        # take below, returns the 0th class's 0th students id.
        #print(studentsinclass[0][0].studentid)

        

        #looping through the number of class objects containing students.
        for i in range(len(studentsinclass)):
            for o in range(len(studentsinclass[i])):
                #print("iteration " + str(o))
                studentdatapacket = StudentData.query.filter_by(studentid=studentsinclass[i][o].studentid).first()
                studentdatapackets.append(studentdatapacket)
                #print(studentdatapacket)
            
        print(studentdatapackets[2].studentid)



        """
        for i in range(0, len(studentsinclass)):
            studentsdata = []
            for o in range(0, len(studentsinclass[i])):
                studentsdata.append(StudentData.query.filter_by(studentid = studentsinclass[i][o].studentid).first())
            
            studentsdatapackets.append(studentsdata)
        
        print(studentsdatapackets)
        print(studentsdatapackets[1][0].studentid)
        """



            
            

        #print(studentsdata[1][0].studentid)

    
   
        print("STUDENTDATA LINE ABOVE")
        studentdatadicts = StudentDataHelper(studentdatapackets);


        print(json.dumps(studentdatadicts))

        #data parsed to javascript script
        json_for_graphs = studentdatadicts
        
        #json.dumps(studentdatadicts)

        #print(studentdatadicts)

        #testClass = Classs.query.filter_by(classcode = "jacob").first()

        
        studentdicts = StudentsInClass(classs);

        


        #print(dicts[0]["students"][0])

        


        if form.validate_on_submit():
            thisClass = Classs();
            thisClass.teacherid = int(current_user.get_id());
            thisClass.classcode = form.class_code.data;

            db.session.add(thisClass)
            db.session.commit()
        
        return render_template('user.html', user=user, form=form, classes=classs, studentdicts=studentdicts, studentdatadicts = studentdatadicts, json_for_graphs=json_for_graphs)  
    else:

        return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')