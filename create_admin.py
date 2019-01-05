from getpass import getpass
import sys

from flask import current_app as app
from werkzeug.security import generate_password_hash
from app import db
from app.models import User

def main():
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            return

        print('Enter username: ') 
        username = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(
            username=username, 
            password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print('User admin added.') 

if __name__ == '__main__':
    sys.exit(main())
