from flask import flash
from models.post import Post


# ────────────────────────────────────────────────────────────────
# helpers
# ────────────────────────────────────────────────────────────────
def _bool_from_form(value):
    return str(value).lower() in {"on", "true", "1"}


# ────────────────────────────────────────────────────────────────
# public API
# ────────────────────────────────────────────────────────────────
def list_posts(*, published: bool):
    return [p for p in Post.get_all() if p.is_published is published]


def get_post(post_id: int):
    return Post.get_by_id(post_id)


def create_post(form) -> bool:
    title = form.get("title", "").strip()
    body = form.get("body", "").strip()
    is_published = _bool_from_form(form.get("is_published"))

    if not title or not body:
        flash("Title and body are required ✏️", "error")
        return False

    Post(title=title, body=body, is_published=is_published)
    flash("Post created successfully ✅", "success")
    return True


def update_post(post_id: int, form) -> bool:
    post = Post.get_by_id(post_id)
    if not post:
        flash("Post not found ❌", "error")
        return False

    title = form.get("title", "").strip()
    body = form.get("body", "").strip()
    is_published = _bool_from_form(form.get("is_published"))

    if not title or not body:
        flash("Title and body cannot be empty ✏️", "error")
        return False

    post.title = title
    post.body = body
    post.is_published = is_published
    flash("Post updated successfully ✅", "success")
    return True


def list_drafts():
    return list_posts(published=False)
