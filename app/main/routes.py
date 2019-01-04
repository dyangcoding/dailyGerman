from flask import Flask, render_template, url_for, redirect, flash, current_app
from app.models import Post
from app.main.forms import ContactForm
from app.main import bp
from app.email import send_email

@bp.route('/')
@bp.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@bp.route('/about')
def about():
    return render_template('about.html', title='About')

@bp.route('/contact')
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        send_email(form.subject.data, form.email.data, \
                    current_app.config['ADMINS'][0], form.message.data)
        flash('your request will be answered as soon as possiable.')
        return redirect(url_for('.home'))
    return render_template('contact.html', title='Contact', form=form)

@bp.route('/<int:post_id>/detail')
def detail(post_id):
    post = Post.query.get(post_id)
    if post is None:
        flash('The Artikel has been removed.')
        return redirect(url_for('.home'))
    return render_template('post_detail.html', post=post)

@bp.route('/posts/interview')
def interview():
    posts = Post.query.filter_by(categorie='Interview').all()
    return render_template('home.html', posts=posts)

@bp.route('/posts/dailyGerman')
def dailyGerman():
    posts = Post.query.filter_by(categorie='German 100').all()
    return render_template('home.html', posts=posts)

@bp.route('/posts/film')
def film():
    posts = Post.query.filter_by(categorie='Film').all()
    return render_template('home.html', posts=posts)

@bp.route('/posts/song')
def song():
    posts = Post.query.filter_by(categorie='Song').all()
    return render_template('home.html', posts=posts)