# this file will handle the login and signup 

from flask import Blueprint,request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from werkzeug.security import generate_password_hash,  check_password_hash
from ...extensions import db
from ...models.user import Role, User
from datetime import datetime


auth_bp=Blueprint("auth",__name__)


@auth_bp.route("/sign-up", methods=["POST"])
def signup():
    data = request.get_json()
    required_fields = ["firstname", "lastname", "email", "password", "recovery_email", "role"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    if data["role"] not in ["recruiter", "job_seeker"]:
        return jsonify({"error": "Invalid role. Must be 'recruiter' or 'job_seeker'"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already registered"}), 400


    dob_str = data.get("dob")  # e.g., "1995-08-20"
    dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
    user = User(
        firstname=data["firstname"],
        lastname=data["lastname"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
        recovery_email=data["recovery_email"],
        phone_no=data.get("phone_no"),
        work_email=data.get("work_email"),
        gender=data.get("gender"),
        dob=dob,
        emp_status=data.get("emp_status")
    )

    role_obj = Role.query.filter_by(name=data["role"]).first()
    if role_obj:
        user.roles.append(role_obj)

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": f"User registered successfully as {data['role']}",
        "user": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "role": data["role"]
        },
        "access_token": access_token
    }), 201


@auth_bp.route("/sign-in", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)

    user_role = user.roles[0].name if user.roles else None

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "role": user_role
        },
        "access_token": access_token
    }), 200
