from flask import Flask, render_template, url_for, redirect, flash
from app.dash.forms import LoginForm, ContactForm, UploadForm, RegistrationForm
from flask_login import login_required
from flask_login import current_user, login_user, logout_user
from app.models import User, Post
from app.dash.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email
from app import app, db

@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/contact')
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        pass
    return render_template('contact.html', title='Contact', form=form)
    
@app.route('/dash/login', methods=['GET', 'POST'])
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

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
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

@app.route('/dash', methods= ['GET', 'POST'])
@login_required
def dash():
    form = UploadForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, categorie=form.categorie.data, content=form.content.data, user_id=current_user.get_id())
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('home'))
    return render_template('dashboard.html', title='Dashboard', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
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

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
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

@app.route('/<int:post_id>/detail')
def detail(post_id):
    post = Post.query.get(post_id)
    if post is None:
        flash('The Artikel has been removed.')
        return redirect(url_for('home'))
    return render_template('post_detail.html', post=post)

@app.route('/posts/interview')
def show_interview_posts():
    posts = Post.query.filter_by(Post.categorie=='Interview').all()
    return render_template('interview_posts.html', posts=posts)

@app.route('/posts/dailyGerman')
def show_daily_posts():
    posts = Post.query.filter_by(Post.categorie=='Daily German 100').all()
    return render_template('dailyGerman_posts.html', posts=posts)

@app.route('/posts/film')
def show_film_posts():
    posts = Post.query.filter_by(Post.categorie=='Film').all()
    return render_template('film_posts.html', posts=posts)