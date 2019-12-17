from flask import render_template, redirect, flash, request, url_for
from flask_login import login_user, logout_user, login_required
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from app import app, db, admin
from .models import  User
from .forms import LoginForm, RegistrationForm

db.create_all()


@app.route('/')
def homepage():
    return render_template('logintest.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html',
                           form=form
                           )


@app.route('/index')
def index():
    return render_template("index.html")


'''''
@app.route('/user/<userId>', methods=['GET', 'POST'])
def user(userId):
    user = Students.query.filter(Students.Id == userId).all()
    return render_template('user.html',
                           title=user.username,
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = StudentForm()
    users = Students.query.all()
    if form.validate_on_submit():
        for user in users:
            if form.username.data == user.username:
                if form.password.data == user.password:
                    return render_template('user.html',
                                           username=user.username,
                                           status=user.status)

                else:
                    flash('password wrong')
                    return redirect('/login')
        flash('no such user')
        return redirect('/login')
    return render_template('login.html',
                           title=login,
                           form=form)


@app.route('/edit/<username>', methods=['GET', 'POST'])
def edit(username):
    user = Students.query.filter(Students.username == username).first()
    form = StudentForm(obj=user)
    if form.validate_on_submit():
        t=user
        t.password = form.password.data
        t.username = form.username.data
        db.session.commit()
        return render_template('user.html',
                        username=user.username)
    return render_template('edit.html',
                           title='change information',
                           form=form)'''''
