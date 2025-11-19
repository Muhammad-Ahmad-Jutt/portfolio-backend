from flask import Flask
from flask_authorize import Authorize
from flask_jwt_extended import JWTManager
from .config import Config
from .extensions import db, migrate
from .api import register_blueprints
from .models.user import User, Role, Permission, Job, JobCategory, JobSalary, JobBatch, JobApplication, Group, user_role, role_permission, user_group

authorize = Authorize()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    authorize.init_app(app)

    # Register your API blueprints
    register_blueprints(app)

    # --------------------------
    # JWT user loader for Flask-Authorize
    # --------------------------
    @jwt.user_lookup_loader
    def load_user(_jwt_header, jwt_data):
        user_id = jwt_data["sub"]  # identity stored in JWT
        return User.query.get(user_id)  # sets current_user for Flask-Authorize

    # Flask-Authorize identity loader
    @authorize.identity_loader
    def current_identity():
        from flask_jwt_extended import current_user as jwt_current_user
        return jwt_current_user

    return app
