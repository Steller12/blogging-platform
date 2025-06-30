from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.post_controller import (
    list_posts, get_post, create_post, update_post, list_drafts
)

post_bp = Blueprint("posts", __name__, url_prefix="/posts")


@post_bp.route("/", methods=["GET"])
def show_posts():
    posts = list_posts(published=True)
    return render_template("posts.html", posts=posts, title="Published Posts")


@post_bp.route("/<int:post_id>", methods=["GET"])
def post_detail(post_id):
    post = get_post(post_id)
    if not post:
        flash("Post not found ❌", "error")
        return redirect(url_for("posts.show_posts"))
    return render_template("post_detail.html", post=post, title=post.title)


@post_bp.route("/new", methods=["GET", "POST"])
def new_post():
    if request.method == "POST":
        if create_post(request.form):
            return redirect(url_for("posts.show_posts"))
    return render_template("post_form.html", post=None, title="New Post")


@post_bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
def edit_post(post_id):
    post = get_post(post_id)
    if not post:
        flash("Post not found ❌", "error")
        return redirect(url_for("posts.show_posts"))

    if request.method == "POST":
        if update_post(post_id, request.form):
            return redirect(url_for("posts.post_detail", post_id=post_id))
    return render_template("post_form.html", post=post, title="Edit Post")


@post_bp.route("/drafts", methods=["GET"])
def drafts():
    drafts = list_drafts()
    return render_template("posts.html", posts=drafts, title="Drafts")
