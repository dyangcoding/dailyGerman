from flask import render_template, url_for, redirect, flash, current_app
from app.models import Post, Message, Comment
from app.main.forms import ContactForm, CommentForm
from app.main import bp
from app import db

@bp.route('/')
@bp.route('/home')
def home():
    posts = Post.query.filter(Post.categorie != 'About').all()
    return render_template('home.html', posts=posts)

@bp.route('/about')
def about():
    about_post = Post.query.filter_by(categorie='About').first()
    return render_template('about.html', title='About', text=about_post.content)

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

@bp.route('/<int:post_id>/detail', methods=['GET', 'POST'])
def detail(post_id):
    post = Post.query.get(post_id)
    if post is None:
        flash('The Artikel does not exist or it has been removed.')
        return redirect(url_for('.home'))
    comments = Comment.query.filter_by(post_id=post_id). \
                order_by(Comment.timestamp.desc()).all()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(author=form.author.data, \
                    comment=form.comment.data, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('your comment is added.')
        new_comments = Comment.query.filter_by(post_id=post_id). \
                order_by(Comment.timestamp.desc()).all()
        return render_template('post_detail.html', post=post, comments=new_comments)
    return render_template('post_detail.html', post=post, comments=comments)

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