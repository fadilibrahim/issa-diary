from flask import (
    render_template,
    url_for,
    redirect,
    request,
    Blueprint,
    session,
    current_app,
)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flask_app import db, bcrypt, mail
from flask_app.models import User, Post
from flask_app.posts.forms import CreatePostForm, EmailForm


posts = Blueprint("posts", __name__)

@posts.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreatePostForm()

    if form.validate_on_submit():
        content = form.text.data

        post = Post(
            title=form.title.data,
            content=content,
            author=current_user,
        )

        db.session.add(post)
        db.session.commit()

        return redirect(url_for("main.index"))

    return render_template(
        "create_post.html", title="Create Post", form=form
    )


@posts.route("/posts/<title>", methods=["GET", "POST"])
def post_detail(title):
    post = Post.query.filter_by(title=title).first()

    return render_template("post_detail.html", post=post)


@posts.route("/posts/email/<title>", methods=["GET", "POST"])
@login_required
def send_post(title):
    form = EmailForm()

    post = Post.query.filter_by(title=title).first()

    if form.validate_on_submit():
        msg = Message(current_user.username + " sent you " + post.title,
                  recipients=[form.email.data])
        msg.body = post.content
        mail.send(msg)

        return render_template("email_sent.html", post=post, form=form)

    return render_template("send_post.html", post=post, form=form)
