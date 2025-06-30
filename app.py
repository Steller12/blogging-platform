import os
from flask import Flask, render_template
from flask_wtf import CSRFProtect

# Initialize extensions
csrf = CSRFProtect()

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    app.config['WTF_CSRF_ENABLED'] = True
    
    # Initialize extensions with app
    csrf.init_app(app)
    
    # Custom template filter for line breaks
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """Convert newlines to HTML line breaks"""
        if text:
            return text.replace('\n', '<br>')
        return text
    
    # Register blueprints
    from routes.post_routes import post_bp
    from routes.auth_routes import auth_bp
    app.register_blueprint(post_bp)
    app.register_blueprint(auth_bp)
    
    @app.route('/')
    def home():
        """Home page - redirect to auth"""
        from controllers.auth_controller import is_logged_in
        if is_logged_in():
            from flask import redirect, url_for
            return redirect(url_for('posts.show_posts'))
        else:
            from flask import redirect, url_for
            return redirect(url_for('auth.login'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
