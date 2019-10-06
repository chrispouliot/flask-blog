from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app
from app.forms import LoginForm
from app.models import User


@app.route("/")
@login_required
def index():
    return render_template(
        "index.html",
        title="title",
        name="name",
        current_user=current_user,
    )


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # User already logged in
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    # POST Request
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.data.password):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        # Add data to session so we know they're logged in
        login_user(user, remember=form.data.remember)
        # Handle redirecting to page they requested when logged out
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':  # netloc not being empty means this is not a relative url
            return redirect(url_for('index'))
        return redirect(url_for(next_page))
    # GET Request
    return render_template('login.html', title='Sign In', form=form)
