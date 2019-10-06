from app import app, db
from app.models import Post, User


@app.shell_context_processor
def context():
    return {'app': app, 'db': db, 'Post': Post, 'User': User}
