from flask import Flask
from flask_authorize import Authorize
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity, current_user as jwt_current_user
from .config import Config
from .extensions import db, migrate
from .api import register_blueprints
from .models.user import User, Role, Permission, Job, JobCategory, JobSalary, JobBatch, JobApplication, Group, user_role, role_permission, user_group
from flask_cors import CORS
from flask_login import LoginManager, login_user

authorize = Authorize()
jwt = JWTManager()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    # --------------------------
    # Config & CORS
    # --------------------------
    app.config.from_object(Config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # --------------------------
    # Initialize extensions
    # --------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)
    authorize.init_app(app)

    # --------------------------
    # Load current_user from JWT before each request
    # --------------------------
    @app.before_request
    def load_jwt_user():
        try:
            # Verify JWT if present
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                user = User.query.get(user_id)
                if user:
                    login_user(user)  # sets current_user for Flask-Login
        except Exception:
            pass  # no JWT, anonymous user

    # --------------------------
    # Flask-Login user loader
    # --------------------------
    @login_manager.user_loader
    def load_user_by_id(user_id):
        return User.query.get(int(user_id))

    # --------------------------
    # Register blueprints & routes
    # --------------------------
    register_blueprints(app)

    @app.route("/")
    def index():
        return {"message": "Welcome to the API homepage!"}

    # --------------------------
    # JWT user loader for Flask-Authorize
    # --------------------------
    @jwt.user_lookup_loader
    def load_user_for_authorize(_jwt_header, jwt_data):
        user_id = jwt_data["sub"]
        return User.query.get(user_id)

    # --------------------------
    # Flask-Authorize identity loader
    # --------------------------
    @authorize.identity_loader
    def current_identity():
        return jwt_current_user

    return app
