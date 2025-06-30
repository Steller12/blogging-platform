# Flask Blog Application
# Routes package

from routes.post_routes import post_bp
from routes.auth_routes import auth_bp

__all__ = ['post_bp', 'auth_bp']