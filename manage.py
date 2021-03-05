#### so if you want to use flask shell and init all the app there
 from main import app, db, User, Post, Tag, migrate


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, User=User, Post =Post, Tag=Tag, migrate=migrate)
