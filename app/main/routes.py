from flask import render_template, url_for, redirect, flash, current_app, request, send_from_directory, make_response
from app.models import Post, Message, Comment
from app.main.forms import ContactForm, CommentForm
from app.main import bp
from app import db, cache
from app.email import send_email

@bp.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@bp.route('/pwabuilder-sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'pwabuilder-sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response

@bp.route('/')
@bp.route('/home')
@cache.cached(300, key_prefix='all_posts')
def home():
    posts = Post.query.filter(Post.categorie != 'About').  \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('display all posts.')
    return render_template('home.html', posts=posts, allPosts=posts)

@bp.route('/about')
@cache.cached(300)
def about():
    about = Post.query.filter_by(categorie='About').first()
    #text = 'Oops, noch kein Inhalt hier !' if about is None else about.content
    current_app.logger.info('display about post.')
    return render_template('about.html', title='About', post=about)

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

@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def showPost(post_id):
    post = Post.query.get(post_id)
    if post is None:
        flash('Der Artikel ist möglichweise gelöscht.')
        return redirect(url_for('.home'))
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(author=form.name.data, \
                    comment=form.comment.data, post_id=post_id)
        comment.save()
        current_app.logger.info('comment user name {}'.format(comment.author))
        flash('Dein Kommentar ist hinzugefügt.')
        send_email(post.id)
        return redirect(request.url)
    return render_template('post_detail.html', post=post, \
                            comments=post.get_comments(), form=form)

@cache.cached(300)
def allPosts():
    return Post.query.filter(Post.categorie != 'About').all()

@bp.route('/posts/working')
@cache.cached(300, key_prefix='working_posts')
def working():
    posts = Post.query.filter_by(categorie='Working'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('display working posts.')
    return render_template('home.html', posts=posts, allPosts=allPosts())

@bp.route('/posts/interview')
@cache.cached(300, key_prefix='interview_posts')
def interview():
    posts = Post.query.filter_by(categorie='Interview'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('display interview posts.')
    return render_template('home.html', posts=posts, allPosts=allPosts())

@bp.route('/posts/dailyGerman')
@cache.cached(300, key_prefix='dailygerman_posts')
def dailyGerman():
    posts = Post.query.filter_by(categorie='DailyGerman'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('display daily german posts.')
    return render_template('home.html', posts=posts, allPosts=allPosts())

@bp.route('/posts/film')
@cache.cached(300, key_prefix='film_posts')
def film():
    posts = Post.query.filter_by(categorie='Film'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('display film posts.')
    return render_template('home.html', posts=posts, allPosts=allPosts())

@bp.route('/posts/song')
@cache.cached(300, key_prefix='song_posts')
def song():
    posts = Post.query.filter_by(categorie='Song'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('disply song posts.')
    return render_template('home.html', posts=posts, allPosts=allPosts())

@bp.route('/posts/friends')
@cache.cached(300, key_prefix='friends_posts')
def friends():
    posts = Post.query.filter_by(categorie='Friends'). \
            order_by(Post.timestamp.desc()).all()
    current_app.logger.info('disply friends posts.')
    return render_template('home.html', posts=posts, allPosts=allPosts())
