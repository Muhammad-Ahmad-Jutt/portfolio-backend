from .v1.users import user_bp
from .v1.auth import auth_bp
# from .v1.projects import project_bp
# from .v1.auth import auth_bp

def register_blueprints(app):
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    # app.register_blueprint(project_bp, url_prefix="/api/v1/projects")
    # app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
