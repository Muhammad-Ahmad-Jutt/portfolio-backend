
from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

from functools import wraps
from flask import jsonify, g
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def permission_required(*permission_numbers): # his function is written with the help ofo ai :https://chatgpt.com/c/693e49bc-8530-832b-9964-c52d31a1dcb0
    """
    Example:
    @permission_required(3001, 3002)
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user:
                return jsonify({"message": "User not found"}), 404

            if user.blocked:
                return jsonify({"message": "User is blocked"}), 403

            user_permission_numbers = {
                perm.per_no
                for role in user.roles
                for perm in role.permissions
            }
            if not set(permission_numbers).intersection(user_permission_numbers):
                return jsonify({"message": "Permission denied"}), 403

            g.current_user = user
            return fn(*args, **kwargs)
        return wrapper
    return decorator
