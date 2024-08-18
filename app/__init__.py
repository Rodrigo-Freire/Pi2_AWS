from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from .config import Config
from .routes import main, user_routes, event_routes

csrf = CSRFProtect()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    csrf.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(user_routes)
    app.register_blueprint(event_routes)

    return app