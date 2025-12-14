# this file will handle the login and signup 

from flask import Blueprint,request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from werkzeug.security import generate_password_hash,  check_password_hash
from ...extensions import db
from ...models.user import Role, User
from datetime import datetime
import re

auth_bp=Blueprint("auth",__name__)


@auth_bp.route("/sign-up", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        required_fields = ["firstname", "lastname", "email", "password", "recovery_email", "role"]
        
        # Check for required fields
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"{field} is required"}), 400
        
        if data["role"] not in ["recruiter", "job_seeker"]:
            return jsonify({"success": False, "message": "Invalid role. Must be 'recruiter' or 'job_seeker'"}), 400

        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"success": False, "message": "Email already registered"}), 400

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, data["email"]):
            return jsonify({"success": False, "message": "Invalid email format"}), 400

        if not re.match(email_regex, data["recovery_email"]):
            return jsonify({"success": False, "message": "Invalid recovery email format"}), 400

        password = data["password"]
        if len(password) < 8:
            return jsonify({"success": False, "message": "Password must be at least 8 characters long"}), 400

        if len(data["firstname"]) > 50 or len(data["lastname"]) > 50:
            return jsonify({"success": False, "message": "Firstname and Lastname must be less than 50 characters"}), 400

        phone_no = data.get("phone_no")
        if phone_no and not re.match(r'^\+?\d{7,15}$', phone_no):
            return jsonify({"success": False, "message": "Invalid phone number format"}), 400

        dob_str = data.get("dob")
        dob = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"success": False, "message": "DOB must be in YYYY-MM-DD format"}), 400

        user = User(
            firstname=data["firstname"],
            lastname=data["lastname"],
            email=data["email"],
            password_hash=generate_password_hash(password),
            recovery_email=data["recovery_email"],
            phone_no=phone_no,
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

        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "success": True,
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

    except Exception as e:
        print('-------------->', e)
        return jsonify({
            "success": False,
            "message": str(e)[:50]  
        }), 500


@auth_bp.route("/sign-in", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({'success':False,"message": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'success':False,"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))

    user_role = user.roles[0].name if user.roles else None

    return jsonify({
        "success":True,
        "message": "Login successful",
        "user": {
            "firstname": user.firstname,
            "role": user_role
        },
        "access_token": access_token
    }), 200
