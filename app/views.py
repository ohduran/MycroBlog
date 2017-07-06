"""Views."""
from flask import render_template, flash, redirect
from flask import session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, EditForm
from .models import User
from datetime import datetime


@lm.user_loader
def load_user(id):
    """Load the user from the database."""
    return User.query.get(int(id))  # Unicode converted into int


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register functionality."""
    """GET"""
    form = LoginForm()
    if request.method == 'GET':
        return render_template('register.html',
                                title='Register',
                                form=form)
    """POST"""
    user = User(username=request.form['username'],
                password=request.form['password'],
                email=request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.before_request
def before_request():
    """Set up a current user."""
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    """Index page."""
    user = current_user
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/user/<username>')
@login_required
def user(username):
    """User page."""
    user = User.query.filter_by(username=username).first()
    if user is None or user == "":
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}]
    return render_template('user.html',
                            user=user,
                            posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    """Edit functionality."""
    form = EditForm()
    if form.validate_on_submit():
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log in functionality."""
    form = LoginForm()
    """GET"""
    if request.method == 'GET':
        return render_template('login.html',
                                title='Sign In',
                                form=form)
    """POST"""
    username = request.form['username']
    password = request.form['password']
    resp = User.query.filter_by(username=username,
                                           password=password).first()
    if resp is None or resp.username == "":
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))
    if form.validate_on_submit():
        login_user(resp)
        flash('Logged in successfully')
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    """Log out functionality."""
    logout_user()
    return redirect(url_for('login'))


@app.errorhandler(404)
def not_found_error(error):
    """Error 404: Not found."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Error 500: Internal."""
    db.session.rollback()  # roll back in ase a working session is needed
    return render_template('500.html'), 500
