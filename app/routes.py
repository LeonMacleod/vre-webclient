from app import app, db
from app.models import Users
from flask import render_template, flash, redirect, request
from app.forms import SignupForm, LoginForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from flask_login import current_user, login_user




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
        return redirect(url_for('index'))
    
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username_or_email.data).first()
        if user is None or not Users.query.filter_by(userpassword=form.userpassword).first():
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Login', form=form)
        




@app.route('/index')
def index():
    return render_template('index.html')