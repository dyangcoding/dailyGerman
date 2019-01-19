import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') \
    or 'k\x80\xec\xb5\xb6\x87d\x19\x96%\r]\x189\xff\xe5\xd36\xa8\x15Gk\x947'
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="fabian082",
    password="diesenweg9527",
    hostname="fabian082.mysql.pythonanywhere-services.com",
    databasename="fabian082$dailyGermanDB",
    )
    SQLALCHEMY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    #MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['dailygerman9527@gmail.com']
    SIMPLEMDE_JS_IIFE = True
    SIMPLEMDE_USE_CDN = True
    FLASK_ADMIN_SWATCH = 'cerulean'
    MAIL_SUPPRESS_SEND = False
    TESTING = False
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True