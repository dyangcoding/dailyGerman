from app import create_app

app = create_app()

# be able to import db after create the instance of db
from app import db
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post' :Post}