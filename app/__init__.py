import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, render_template, url_for, redirect, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_simplemde import SimpleMDE
from flask_misaka import Misaka
from flask_admin import Admin, expose, AdminIndexView, helpers
from flask_admin.contrib.sqla import ModelView
from flask_caching import Cache
from flask_sslify import SSLify
from config import Config
from .forms import LoginForm

migrate = Migrate()
db = SQLAlchemy()
admin = Admin()
login = LoginManager()
login.session_protection = 'strong'
login.login_view = 'login'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
md = Misaka()
cache = Cache(config={'CACHE_TYPE': 'simple'})

class DGAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('.login'))
        return super(DGAdminIndexView, self).index()

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm()
        if helpers.validate_form_on_submit(form):
            from .models import User
            user = User.query.filter_by(username=form.username.data).first()
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('.login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('.index'))
        return render_template('login.html', form=form)

    @expose('/logout')
    @login_required
    def logout(self):
        logout_user()
        return redirect(url_for('.login'))

class UserModeView(ModelView):
    def is_accessible(self):
        if (not current_user.is_active or not
                current_user.is_authenticated):
            return False
        return True

class PostModeView(ModelView):
    def is_accessible(self):
        if (not current_user.is_active or not
                current_user.is_authenticated):
            return False
        return True

class MessageModeView(ModelView):
    def is_accessible(self):
        if (not current_user.is_active or not
                current_user.is_authenticated):
            return False
        return True

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    from .models import User
    from .models import Post
    from .models import Message
    admin.init_app(app, index_view=DGAdminIndexView())
    admin.add_view(UserModeView(User, db.session))
    admin.add_view(PostModeView(Post, db.session))
    admin.add_view(MessageModeView(Message, db.session))
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    SimpleMDE(app)
    md.init_app(app)
    cache.init_app(app)
    SSLify(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as error_bp
    app.register_blueprint(error_bp)

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='DailyGerman Failure',
                credentials=auth)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/dailyGerman.log', maxBytes=10240,
                                            backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('DailyGerman startup')

    return app

from app import models
