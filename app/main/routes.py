from flask import render_template, url_for, redirect, flash
from app.models import Post, Message
from app.main.forms import ContactForm
from app.main import bp
from app import db

@bp.route('/')
@bp.route('/home')
def home():
    posts = Post.query.filter(Post.categorie != 'About').all()
    return render_template('home.html', posts=posts)

@bp.route('/about')
def about():
    about = Post.query.filter_by(categorie='About').first()
    text = 'Oops, noch kein Inhalt hier !' if about is None else about.content
    return render_template('about.html', title='About', text=text)

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = Message(sender_name=form.name.data, sender_email=form.email.data, \
                            subject=form.subject.data, message_body=form.message.data)
        db.session.add(msg)
        db.session.commit()
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
    posts = Post.query.filter_by(categorie='DailyGerman').all()
    return render_template('home.html', posts=posts)

@bp.route('/posts/film')
def film():
    posts = Post.query.filter_by(categorie='Film').all()
    return render_template('home.html', posts=posts)

@bp.route('/posts/song')
def song():
    posts = Post.query.filter_by(categorie='Song').all()
    return render_template('home.html', posts=posts)