from app import create_app
from app.models import db
from app.models import User, Post
from getpass import getpass
from werkzeug.security import generate_password_hash

app = create_app()

def create_admin():
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            return

        print('Enter username: ')
        username = input()
        print('Enter email: ')
        email = input()
        password = getpass()
        assert password == getpass('Password (again):')

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print('User admin added.')

create_admin()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post' :Post}