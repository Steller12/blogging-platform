from models.post import Post
from flask import flash, redirect, url_for

def list_posts(published):
    """
    TODO: Query Post model filtered by is_published status.
    Return a list of posts.
    """
    pass
def get_post(post_id):
    """
    TODO: Retrieve a post by its ID or abort with 404 if not found.
    """
    pass
def create_post(form):
    """
    TODO: Extract title, body, and is_published from form.
    Validate fields, flash errors, save new Post, flash success, redirect.
    """
    pass
def update_post(post_id, form):
    """
    TODO: Fetch existing post, update attributes from form,
    validate, save changes, flash messages, and redirect.
    """
    pass
def list_drafts():
    """
    TODO: Reuse list_posts to fetch unpublished posts.
    """
    pass