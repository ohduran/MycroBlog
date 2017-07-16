"""Views."""
from flask import render_template, flash, redirect
from flask import session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, EditForm, PostForm, SearchForm
from .models import User, Post
from datetime import datetime
from config import POSTS_PER_PAGE


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
    if request.method == 'POST':
        # Look for the post information on the database
        username_used = User.query.filter_by(
            username=request.form['username']).first()
        email_used = User.query.filter_by(
            email=request.form['email']).first()
        # If user already exists
        if username_used is not None:
            flash('Username already in use. Try a different username.')
            return redirect(url_for('register'))
        # If email already in use.
        if email_used is not None:
            flash('Email already in use. Try a different email.')
            return redirect(url_for('register'))
    user = User(username=request.form['username'],
                password=request.form['password'],
                email=request.form['email'])
    db.session.add(user)
    db.session.commit()
    user.follow(user)
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))


@app.before_request
def before_request():
    """Set up a current user."""
    g.user = current_user
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()
        current_user.search_form = SearchForm()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
@login_required
def index(page=1):
    """Index page."""
    user = current_user
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data,
                    timestamp=datetime.utcnow(),
                    author=user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been sent!')
        return redirect(url_for('index'))

    # page number, items per page, False means no error, just empty list.
    posts = user.get_followed_posts().paginate(
        page, POSTS_PER_PAGE, False)
    return render_template("index.html",
                           title='Home',
                           user=user,
                           form=form,
                           posts=posts)


@app.route('/user/<username>')
@app.route('/user/<username>/<int:page>')
@login_required
def user(username, page=1):
    """User page."""
    user = User.query.filter_by(username=username).first()
    if user is None or user == "":
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    # posts = [
    #     {'author': user, 'body': 'Test post #1'},
    #     {'author': user, 'body': 'Test post #2'}]
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                            user=user,
                            posts=posts)


@app.route('/search', methods=['POST'])
@login_required
def search():
    """Search engine."""
    if not current_user.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results',
                            query=current_user.search_form.search.data))


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


@app.route('/follow/<username>')
@login_required
def follow(username):
    """Follow a user."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    elif user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', username=username))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + username + '!')
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + username + '!')
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    """Unfollow a user."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', username=username))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + username + '.')
        return redirect(url_for('user', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + username + '.')
    return redirect(url_for('user', username=username))


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
