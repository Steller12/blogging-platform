import os
import json
from datetime import datetime
from flask import flash, redirect, url_for, abort, current_app
from controllers.auth_controller import get_current_user

# File paths for storing data
POSTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts.json')
TAGS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tags.json')

def load_posts():
    """Load posts from JSON file"""
    try:
        if os.path.exists(POSTS_FILE):
            with open(POSTS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        current_app.logger.error(f'Error loading posts: {str(e)}')
    return []

def save_posts(posts):
    """Save posts to JSON file"""
    try:
        with open(POSTS_FILE, 'w') as f:
            json.dump(posts, f, indent=2)
        return True
    except Exception as e:
        current_app.logger.error(f'Error saving posts: {str(e)}')
        return False

def load_tags():
    """Load tags from JSON file"""
    try:
        if os.path.exists(TAGS_FILE):
            with open(TAGS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        current_app.logger.error(f'Error loading tags: {str(e)}')
    return []

def save_tags(tags):
    """Save tags to JSON file"""
    try:
        with open(TAGS_FILE, 'w') as f:
            json.dump(tags, f, indent=2)
        return True
    except Exception as e:
        current_app.logger.error(f'Error saving tags: {str(e)}')
        return False

def get_next_post_id():
    """Get next available post ID"""
    posts = load_posts()
    if not posts:
        return 1
    return max(post['id'] for post in posts) + 1

class Post:
    """Simple Post class for file-based storage"""
    def __init__(self, id, title, body, author, is_published=False, tags=None, created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.body = body
        self.author = author
        self.is_published = is_published
        self.tags = tags or []
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'author': self.author,
            'is_published': self.is_published,
            'tags': self.tags,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)
    
    def publish(self):
        if self.is_published:
            raise ValueError("Post is already published")
        self.is_published = True
        self.updated_at = datetime.now().isoformat()
    
    def unpublish(self):
        if not self.is_published:
            raise ValueError("Post is already unpublished")
        self.is_published = False
        self.updated_at = datetime.now().isoformat()

def list_posts(published=True):
    """
    Get posts filtered by is_published status.
    Return a list of posts ordered by creation date (newest first).
    """
    posts_data = load_posts()
    posts = [Post.from_dict(data) for data in posts_data]
    
    # Filter by published status
    filtered_posts = [post for post in posts if post.is_published == published]
    
    # Sort by created_at (newest first)
    filtered_posts.sort(key=lambda x: x.created_at, reverse=True)
    
    return filtered_posts

def get_post(post_id):
    """
    Retrieve a post by its ID or abort with 404 if not found.
    """
    posts_data = load_posts()
    
    for data in posts_data:
        if data['id'] == int(post_id):
            return Post.from_dict(data)
    
    abort(404)

def create_post(form_data):
    """
    Extract title, body, and is_published from form data.
    Create new post, validate, save, flash messages, and redirect.
    """
    try:
        # Get the current authenticated user
        user = get_current_user()
        if not user:
            flash('You must be logged in to create a post.', 'error')
            return redirect(url_for('auth.login'))
        
        # Load existing posts
        posts_data = load_posts()
        
        # Create new post
        new_post = Post(
            id=get_next_post_id(),
            title=form_data.get('title', '').strip(),
            body=form_data.get('body', '').strip(),
            author=user['username'],
            is_published=bool(form_data.get('is_published')),
            tags=form_data.getlist('tags') if hasattr(form_data, 'getlist') else form_data.get('tags', [])
        )
        
        # Add to posts list
        posts_data.append(new_post.to_dict())
        
        # Save posts
        if save_posts(posts_data):
            flash('Post created successfully!', 'success')
            if new_post.is_published:
                return redirect(url_for('posts.show_posts'))
            else:
                return redirect(url_for('posts.drafts'))
        else:
            flash('Error creating post. Please try again.', 'error')
            return redirect(url_for('posts.new_post'))
            
    except Exception as e:
        current_app.logger.error(f'Error creating post: {str(e)}')
        flash(f'Error creating post: {str(e)}', 'error')
        return redirect(url_for('posts.new_post'))

def update_post(post_id, form_data):
    """
    Fetch existing post, update attributes from form data,
    validate, save changes, flash messages, and redirect.
    """
    try:
        posts_data = load_posts()
        
        # Find and update post
        for i, data in enumerate(posts_data):
            if data['id'] == int(post_id):
                post = Post.from_dict(data)
                
                # Update post fields
                post.title = form_data.get('title', '').strip()
                post.body = form_data.get('body', '').strip()
                post.is_published = bool(form_data.get('is_published'))
                post.tags = form_data.getlist('tags') if hasattr(form_data, 'getlist') else form_data.get('tags', [])
                post.updated_at = datetime.now().isoformat()
                
                # Replace in list
                posts_data[i] = post.to_dict()
                
                # Save posts
                if save_posts(posts_data):
                    flash('Post updated successfully!', 'success')
                    if post.is_published:
                        return redirect(url_for('posts.show_posts'))
                    else:
                        return redirect(url_for('posts.drafts'))
                else:
                    flash('Error updating post. Please try again.', 'error')
                    return redirect(url_for('posts.edit_post', post_id=post_id))
        
        # Post not found
        abort(404)
            
    except Exception as e:
        current_app.logger.error(f'Error updating post: {str(e)}')
        flash(f'Error updating post: {str(e)}', 'error')
        return redirect(url_for('posts.edit_post', post_id=post_id))

def delete_post(post_id):
    """
    Delete a post by ID.
    """
    try:
        posts_data = load_posts()
        
        # Find and remove post
        for i, data in enumerate(posts_data):
            if data['id'] == int(post_id):
                posts_data.pop(i)
                
                if save_posts(posts_data):
                    flash('Post deleted successfully!', 'success')
                else:
                    flash('Error deleting post. Please try again.', 'error')
                return redirect(url_for('posts.show_posts'))
        
        # Post not found
        abort(404)
        
    except Exception as e:
        current_app.logger.error(f'Error deleting post: {str(e)}')
        flash(f'Error deleting post: {str(e)}', 'error')
        return redirect(url_for('posts.show_posts'))

def list_drafts():
    """
    Reuse list_posts to fetch unpublished posts.
    """
    return list_posts(published=False)

def publish_post(post_id):
    """
    Publish a post using the post's publish method.
    """
    try:
        posts_data = load_posts()
        
        # Find and publish post
        for i, data in enumerate(posts_data):
            if data['id'] == int(post_id):
                post = Post.from_dict(data)
                post.publish()
                posts_data[i] = post.to_dict()
                
                if save_posts(posts_data):
                    flash(f'Post "{post.title}" published successfully!', 'success')
                else:
                    flash('Error publishing post. Please try again.', 'error')
                return redirect(url_for('posts.show_posts'))
        
        # Post not found
        abort(404)
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('posts.drafts'))
    except Exception as e:
        current_app.logger.error(f'Error publishing post: {str(e)}')
        flash(f'Error publishing post: {str(e)}', 'error')
        return redirect(url_for('posts.drafts'))

def unpublish_post(post_id):
    """
    Unpublish a post using the post's unpublish method.
    """
    try:
        posts_data = load_posts()
        
        # Find and unpublish post
        for i, data in enumerate(posts_data):
            if data['id'] == int(post_id):
                post = Post.from_dict(data)
                post.unpublish()
                posts_data[i] = post.to_dict()
                
                if save_posts(posts_data):
                    flash(f'Post "{post.title}" moved to drafts!', 'success')
                else:
                    flash('Error unpublishing post. Please try again.', 'error')
                return redirect(url_for('posts.drafts'))
        
        # Post not found
        abort(404)
        
    except ValueError as e:
        flash(str(e), 'error')
        return redirect(url_for('posts.show_posts'))
    except Exception as e:
        current_app.logger.error(f'Error unpublishing post: {str(e)}')
        flash(f'Error unpublishing post: {str(e)}', 'error')
        return redirect(url_for('posts.show_posts'))

def get_all_tags():
    """
    Get all available tags for forms.
    """
    try:
        tags_data = load_tags()
        # Return simple objects with name attribute
        class Tag:
            def __init__(self, name):
                self.name = name
        
        return [Tag(tag) for tag in tags_data]
    except Exception:
        return []
