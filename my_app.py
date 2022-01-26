from app import app, db
from app.models import User, Post, Notification, Message


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        User=User,
        Post=Post,
        Notification=Notification,
        Message=Message
    )
