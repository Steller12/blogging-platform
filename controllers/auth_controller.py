import os
from flask import flash, redirect, url_for, current_app, session, request

# File path for storing user data
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.txt')

def load_users():
    """Load users from text file"""
    users = {}
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and ',' in line:
                        parts = line.split(',')
                        if len(parts) >= 3:
                            username, email, password = parts[0], parts[1], parts[2]
                            users[email] = {
                                'username': username,
                                'email': email,
                                'password': password
                            }
    except Exception as e:
        current_app.logger.error(f'Error loading users: {str(e)}')
    return users

def save_user(username, email, password):
    """Save new user to text file"""
    try:
        with open(USERS_FILE, 'a') as f:
            f.write(f'{username},{email},{password}\n')
        return True
    except Exception as e:
        current_app.logger.error(f'Error saving user: {str(e)}')
        return False

def login_user(form_data):
    """
    Authenticate user with email and password.
    Set user session if successful.
    """
    try:
        email = form_data.get('email', '').strip().lower()
        password = form_data.get('password', '')
        remember_me = form_data.get('remember_me', False)
        
        users = load_users()
        
        # Find user by email
        user = users.get(email)
        
        if user and user['password'] == password:
            # Set user session
            session['user_id'] = email  # Use email as ID
            session['username'] = user['username']
            session['email'] = user['email']
            session.permanent = bool(remember_me)
            
            flash(f'Welcome back, {user["username"]}!', 'success')
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('posts.show_posts'))
        else:
            flash('Invalid email or password. Please try again.', 'error')
            return redirect(url_for('auth.login'))
            
    except Exception as e:
        current_app.logger.error(f'Error during login: {str(e)}')
        flash('An error occurred during login. Please try again.', 'error')
        return redirect(url_for('auth.login'))

def register_user(form_data):
    """
    Create a new user account with validation.
    """
    try:
        username = form_data.get('username', '').strip()
        email = form_data.get('email', '').strip().lower()
        password = form_data.get('password', '')
        
        users = load_users()
        
        # Check if user already exists
        if email in users:
            flash('Email already registered. Please use a different email.', 'error')
            return redirect(url_for('auth.signup'))
        
        # Check if username already exists
        for user_data in users.values():
            if user_data['username'] == username:
                flash('Username already exists. Please choose a different one.', 'error')
                return redirect(url_for('auth.signup'))
        
        # Save new user
        if save_user(username, email, password):
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('An error occurred while creating your account. Please try again.', 'error')
            return redirect(url_for('auth.signup'))
        
    except Exception as e:
        current_app.logger.error(f'Error creating user account: {str(e)}')
        flash('An error occurred while creating your account. Please try again.', 'error')
        return redirect(url_for('auth.signup'))

def logout_user():
    """
    Clear user session and redirect to login.
    """
    try:
        username = session.get('username', 'User')
        session.clear()
        flash(f'Goodbye, {username}! You have been logged out.', 'info')
        return redirect(url_for('auth.login'))
        
    except Exception as e:
        current_app.logger.error(f'Error during logout: {str(e)}')
        session.clear()  # Clear session anyway
        flash('You have been logged out.', 'info')
        return redirect(url_for('auth.login'))

def get_current_user():
    """
    Get current user from session.
    Returns user dict or None if not logged in.
    """
    user_id = session.get('user_id')
    if not user_id:
        return None
    
    try:
        users = load_users()
        return users.get(user_id)
    except Exception:
        return None

def is_logged_in():
    """
    Check if user is currently logged in.
    """
    return 'user_id' in session

def require_login():
    """
    Decorator function to require login for protected routes.
    """
    if not is_logged_in():
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.login', next=request.url))
    return None
