import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') \
    or 'k\x80\xec\xb5\xb6\x87d\x19\x96%\r]\x189\xff\xe5\xd36\xa8\x15Gk\x947'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="fabian082",
    password="a15803449527",
    hostname="fabian082.mysql.pythonanywhere-services.com",
    databasename="fabian082$dailyGermanDB",
    )
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('smtp.gmail.com')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['dailygerman9527@gmail.com']
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    FLASK_ADMIN_SWATCH = 'cerulean'