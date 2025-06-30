from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers.post_controller import (
    list_posts, get_post, create_post, update_post, list_drafts, 
    delete_post, publish_post, unpublish_post, get_all_tags
)
from controllers.auth_controller import require_login, is_logged_in
from forms.post_form import PostForm
from forms.email_form import EmailForm

post_bp = Blueprint('posts', __name__, url_prefix='/posts')

@post_bp.route('/', methods=['GET'])
def show_posts():
    """
    Retrieve published posts and render 'posts.html' with the posts list.
    """
    posts = list_posts(published=True)
    return render_template('posts.html', posts=posts, page_title="Published Posts")

@post_bp.route('/<int:post_id>', methods=['GET'])
def post_detail(post_id):
    """
    Fetch a single post by ID and render 'post_detail.html' with the post.
    """
    post = get_post(post_id)
    return render_template('post_detail.html', post=post)

@post_bp.route('/new', methods=['GET', 'POST'])
def new_post():
    """
    Create new post using WTForms.
    On GET, render 'post_form.html' with form.
    On POST, validate form and create post.
    """
    # Check if user is logged in
    auth_check = require_login()
    if auth_check:
        return auth_check
    
    form = PostForm()
    
    # Populate tag choices
    tags = get_all_tags()
    form.tags.choices = [(tag.name, tag.name) for tag in tags]
    
    if form.validate_on_submit():
        # Convert form data to dict-like object for controller
        form_data = {
            'title': form.title.data,
            'body': form.body.data,
            'is_published': form.is_published.data,
            'tags': form.tags.data
        }
        # Create a simple object to simulate request.form.getlist
        class FormData:
            def get(self, key, default=''):
                return form_data.get(key, default)
            def getlist(self, key):
                return form_data.get(key, [])
        
        return create_post(FormData())
    
    return render_template('post_form.html', form=form, post=None, page_title="Create New Post")

@post_bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(post_id):
    """
    Edit existing post using WTForms.
    On GET, fetch post and render 'post_form.html' with populated form.
    On POST, validate form and update post.
    """
    # Check if user is logged in
    auth_check = require_login()
    if auth_check:
        return auth_check
    
    post = get_post(post_id)
    form = PostForm(obj=post)
    
    # Populate tag choices
    tags = get_all_tags()
    form.tags.choices = [(tag.name, tag.name) for tag in tags]
    
    # Pre-select current tags
    if request.method == 'GET':
        form.tags.data = [tag.name for tag in post.tags]
    
    if form.validate_on_submit():
        # Convert form data to dict-like object for controller
        form_data = {
            'title': form.title.data,
            'body': form.body.data,
            'is_published': form.is_published.data,
            'tags': form.tags.data
        }
        # Create a simple object to simulate request.form.getlist
        class FormData:
            def get(self, key, default=''):
                return form_data.get(key, default)
            def getlist(self, key):
                return form_data.get(key, [])
        
        return update_post(post_id, FormData())
    
    return render_template('post_form.html', form=form, post=post, page_title="Edit Post")

@post_bp.route('/drafts', methods=['GET'])
def drafts():
    """
    Retrieve unpublished posts and render 'posts.html' with the drafts list.
    """
    # Check if user is logged in
    auth_check = require_login()
    if auth_check:
        return auth_check
    
    drafts = list_drafts()
    return render_template('posts.html', posts=drafts, page_title="Draft Posts")

@post_bp.route('/<int:post_id>/delete', methods=['POST'])
def delete_post_route(post_id):
    """
    Delete a post.
    """
    return delete_post(post_id)

@post_bp.route('/<int:post_id>/publish', methods=['POST'])
def publish_post_route(post_id):
    """
    Publish a draft post using the post's publish method.
    """
    return publish_post(post_id)

@post_bp.route('/<int:post_id>/unpublish', methods=['POST'])
def unpublish_post_route(post_id):
    """
    Unpublish a published post using the post's unpublish method.
    """
    return unpublish_post(post_id)

@post_bp.route('/email-test', methods=['GET', 'POST'])
def email_test():
    """
    Test email validation functionality.
    """
    form = EmailForm()
    
    if form.validate_on_submit():
        try:
            from models.user import User
            
            # Test creating a user with the provided email
            user = User(username=form.username.data)
            user.email = form.email.data  # This will trigger validation
            # Don't actually save, just test validation
            flash(f'Email validation successful for: {form.email.data}', 'success')
        except ValueError as e:
            flash(f'Email validation failed: {str(e)}', 'error')
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('email_test.html', form=form)
