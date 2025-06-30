from flask import Flask
from routes.post_routes import post_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "change‑me"
    app.register_blueprint(post_bp)
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
