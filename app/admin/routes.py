from flask import render_template, url_for, redirect, flash
from app.admin.forms import LoginForm, UploadForm, RegistrationForm
from flask_login import login_required
from flask_login import current_user, login_user, logout_user
from app.models import User, Post
from app.admin.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.admin import bp
from app.admin.email import send_password_reset_email
from app.models import db

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@bp.route('/dash/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('dash'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dash'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@bp.route('/dash', methods= ['GET', 'POST'])
@login_required
def dash():
    form = UploadForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, categorie=form.categorie.data, 
                    content=form.content.data, user_id=current_user.get_id())
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('home'))
    return render_template('dashboard.html', title='Dashboard', form=form)

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)