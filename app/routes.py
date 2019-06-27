from app import app, db
from app.models import Users
from flask import render_template, flash, redirect, request
from app.forms import LoginForm
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()

    if form.validate_on_submit():

        user = Users()
        user.username = form.username.data;
        user.password = form.password.data;
        user.useremail = form.email.data;

        db.session.add(user)
        db.session.commit()
        

        flash('Login requested for user{}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')


        





    return render_template('signup.html', title='Sign Up', form=form)




@app.route('/index')
def index():
    return render_template('index.html')