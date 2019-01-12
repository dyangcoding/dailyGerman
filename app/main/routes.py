from flask import render_template, url_for, redirect, flash, current_app
from app.models import Post, Message
from app.main.forms import ContactForm
from app.main import bp
from app import db, cache

@bp.route('/')
@bp.route('/home')
@cache.cached(300, key_prefix='all_posts')
def home():
    posts = Post.query.filter(Post.categorie != 'About').all()
    current_app.logger.info('display all posts.')
    return render_template('home.html', posts=posts)

@bp.route('/about')
@cache.cached(300)
def about():
    about = Post.query.filter_by(categorie='About').first()
    text = 'Oops, noch kein Inhalt hier !' if about is None else about.content
    current_app.logger.info('display about post.')
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
@cache.cached(300, key_prefix='interview_posts')
def interview():
    posts = Post.query.filter_by(categorie='Interview'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('display interview posts.')
    return render_template('home.html', posts=posts)

@bp.route('/posts/dailyGerman')
@cache.cached(300, key_prefix='dailygerman_posts')
def dailyGerman():
    posts = Post.query.filter_by(categorie='DailyGerman'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('display daily german posts.')
    return render_template('home.html', posts=posts)

@bp.route('/posts/film')
@cache.cached(300, key_prefix='film_posts')
def film():
    posts = Post.query.filter_by(categorie='Film'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('display film posts.')
    return render_template('home.html', posts=posts)

@bp.route('/posts/song')
@cache.cached(300, key_prefix='song_posts')
def song():
    posts = Post.query.filter_by(categorie='Song'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('disply song posts.')
    return render_template('home.html', posts=posts)