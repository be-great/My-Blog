
from flask import Flask ,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevConfig
from sqlalchemy import func, desc
from flask import Flask, render_template, flash, redirect, url_for
from forms import CommentForm
from flask_admin import Admin
app = Flask(__name__)
app.config.from_object(DevConfig)
admin = Admin(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
import models
from models import Post ,Tag , tags , Comment ,User


##################helping functions###################################
def sidebar_data():
    recent = Post.query.order_by(Post.publish_date.desc()).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.post_id).label('total')
    ).join(tags).group_by(Tag).order_by(desc('total')).limit(5).all()

    return recent, top_tags

######################################################################
@app.route('/')
@app.route('/<int:page>')
def home(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, app.config.get('POSTS_PER_PAGE', 10), False)
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html',
        posts=posts,
        recent=recent,
        top_tags=top_tags
    )

@app.route('/post/<int:post_id>',methods=('GET','POST'))
def post(post_id):
    form = CommentForm() # in forms.py
    # add comment to table comments , if all the validate happend after submit
    if form.validate_on_submit():
        new_comment =Comment() # in models.py
        new_comment.name =form.name.data
        new_comment.text =form.text.data
        new_comment.post_id=post_id
        try :
            db.session.add(new_comment)
            db.session.commit()
        except Exception as e :
            flash("Error adding your comment : %s" % str(e),'error')
            db.session.rollback()
        else:
            flash('Comment added','info')
        return redirect(url_for('post',post_id=post_id))
    # get the post id
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    comments = post.comments.order_by(Comment.date.desc()).all() #
    recent,top_tags=sidebar_data()
    return render_template('post.html',
    post=post,
    tags=tags,
    comments=comments,
    recent=recent,
    top_tags=top_tags,
    form=form)

@app.route('/posts_by_user/<string:username>',methods=["GET"])
def posts_by_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts.order_by(Post.publish_date.desc()).all()
    recent , top_tags = sidebar_data()
    return render_template('user.html',
    user=user,
    posts=posts,
    recent=recent,
    top_tags=top_tags
    )


@app.route('/posts_by_tag/<string:tag_name>',methods=['GET'])
def posts_by_tag(tag_name):
    tag = Tag.query.filter_by(title=tag_name).first_or_404()
    posts = tag.posts.order_by(Post.publish_date.desc()).all()
    recent , top_tags = sidebar_data()
    return render_template('tag.html',
    tag=tag,
    posts=posts,
    recent=recent,
    top_tags=top_tags
    )
from flask_admin.contrib.sqla import ModelView
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Post,db.session))
admin.add_view(ModelView(Tag,db.session))
admin.add_view(ModelView(Comment,db.session))
if __name__ == '__main__':
    app.run()
