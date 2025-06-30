from flask import Blueprint, render_template, request, redirect, url_for
from controllers import auth_controller
from forms.auth_form import LoginForm, SignupForm

# Create blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page and handler"""
    # If user is already logged in, redirect to posts
    if auth_controller.is_logged_in():
        return redirect(url_for('posts.show_posts'))
    
    form = LoginForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            return auth_controller.login_user(form.data)
        else:
            # Flash form errors
            for field, errors in form.errors.items():
                for error in errors:
                    from flask import flash
                    flash(f'{field.title()}: {error}', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page and handler"""
    # If user is already logged in, redirect to posts
    if auth_controller.is_logged_in():
        return redirect(url_for('posts.show_posts'))
    
    form = SignupForm()
    
    if request.method == 'POST':
        if form.validate_on_submit():
            return auth_controller.register_user(form.data)
        else:
            # Flash form errors
            for field, errors in form.errors.items():
                for error in errors:
                    from flask import flash
                    flash(f'{field.title()}: {error}', 'error')
    
    return render_template('auth/signup.html', form=form)

@auth_bp.route('/logout')
def logout():
    """Logout handler"""
    return auth_controller.logout_user()

@auth_bp.route('/')
def index():
    """Redirect to login if not authenticated, otherwise to posts"""
    if auth_controller.is_logged_in():
        return redirect(url_for('posts.show_posts'))
    return redirect(url_for('auth.login'))
