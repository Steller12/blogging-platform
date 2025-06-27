from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.post_controller import (
    list_posts, get_post, create_post, update_post, list_drafts
)
post_bp = Blueprint('posts', __name__, url_prefix='/posts')
@post_bp.route('/', methods=['GET'])
def show_posts():
    """
    TODO: Retrieve published posts via list_posts(published=True)
    and render 'posts.html' with the posts list.
    """
    pass

@post_bp.route('/<int:post_id>', methods=['GET'])
def post_detail(post_id):
    """
    TODO: Fetch a single post by ID using get_post(post_id)
    and render 'post_detail.html' with the post.
    """
    pass

@post_bp.route('/new', methods=['GET', 'POST'])
def new_post():
    """
    TODO: On GET, render 'post_form.html'.
    On POST, collect form data from request.form and call create_post(form).
    """
    pass

@post_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """
    TODO: On GET, fetch post and render 'post_form.html' with post data.
    On POST, collect form data and call update_post(post_id, form).
    """
    pass

@post_bp.route('/drafts', methods=['GET'])
def drafts():
    """
    TODO: Retrieve unpublished posts via list_drafts()
    and render 'posts.html' with the drafts list.
    """
    pass