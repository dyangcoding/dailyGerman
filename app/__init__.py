import logging, os
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_simplemde import SimpleMDE
from flask_misaka import Misaka
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from config import Config

migrate = Migrate()
db = SQLAlchemy()
admin = Admin()
login = LoginManager()
login.session_protection = 'strong'
login.login_view = 'login'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    migrate.init_app(app)
    db.init_app(app)
    from .models import User
    from .models import Post
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Post, db.session))
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    SimpleMDE(app)
    Misaka(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    """ from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin') """

    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='DailyGerman Failure',
                credentials=auth, secure=secure)
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
