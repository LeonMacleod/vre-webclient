from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for user{}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect('/index')


        





    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/index')
def index():
    return render_template('index.html')