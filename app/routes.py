from app import app, db
from app.models import Users
from flask import render_template, flash, redirect, request
from app.forms import SignupForm, LoginForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length




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

    if form.validate_on_submit():
    

        username = ""
        

        userbyname = Users.query.filter_by(username=form.username_or_email.data).first()
        if(userbyname is None):
            userbyemail = Users.query.filter_by(useremail=form.username_or_email.data).first()

            if(userbyemail is None):
                print("Entered username or email is not an email.")
                #raise ValidationError("USER DOES NOT EXIST!")
            else:
                username = userbyemail
        else:
            username = userbyname
    
        

        userpassword = Users.query.filter_by(password=form.password.data).first()
        if(userpassword is None):
            print("The provided password was not valid.")
        else:
            if(userpassword.username == username):
                return redirect("/signup")
        

        



        return redirect('/signup')
    return render_template('login.html', title='Log In', form=form)



@app.route('/index')
def index():
    return render_template('index.html')