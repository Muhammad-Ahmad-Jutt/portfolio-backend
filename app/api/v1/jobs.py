# this file will handle the login and signup 

from flask import Blueprint,request, jsonify
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from ...extensions import db
from ...models.user import Role, User,JobCategory,Job
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity#, current_user
from flask_login import current_user,login_required
job_bp=Blueprint("jobs",__name__)




job_bp = Blueprint("jobs", __name__)

# ---------------------------
# CREATE a Job
# ---------------------------

@job_bp.route("/job", methods=["POST"])
@jwt_required()  # ensures the user is logged in via JWT/Flask-Login

def create_job():
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    active_date_str = data.get("active_date")
    active_till_str = data.get("active_till")
    job_category_id = data.get("job_category_id")

    if not all([title, description, active_date_str, active_till_str, job_category_id]):
        return jsonify({"error": "Missing required fields"}), 400

    # Convert string to Python date
    try:
        active_date = datetime.strptime(active_date_str, "%Y-%m-%d").date()
        active_till = datetime.strptime(active_till_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Dates must be in YYYY-MM-DD format"}), 400

    # Ensure job category exists
    job_category = JobCategory.query.get(job_category_id)
    if not job_category:
        return jsonify({"error": "Job category not found"}), 404

    job = Job(
        title=title,
        description=description,
        active_date=active_date,
        active_till=active_till,
        job_category_id=job_category_id,
        user_id=current_user.id,
    )

    db.session.add(job)
    db.session.commit()

    return jsonify({
        "message": "Job created successfully",
        "job": {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "active_date": str(job.active_date),
            "active_till": str(job.active_till),
            "job_category_id": job.job_category_id,
            "user_id": job.user_id
        }
    }), 201


# ---------------------------
# READ all Jobs
# ---------------------------
@job_bp.route("/job", methods=["GET"])
@jwt_required()
def get_all_jobs():
    jobs = Job.query.all()
    result = []
    for job in jobs:
        result.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "active": job.active,
            "accepting_applicant": job.accepting_applicant,
            "posted_date": job.posted_date.isoformat(),
            "job_category": job.job_category.category_name if job.job_category else None,
            "user_id": job.user_id
        })
    return jsonify(result), 200


# ---------------------------
# READ single Job
# ---------------------------
@job_bp.route("/job/<int:id>", methods=["GET"])
@jwt_required()
def get_job(id):
    job = Job.query.get(id)
    if not job:
        return jsonify({"message": "Job not found"}), 404

    result = {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "active": job.active,
        "accepting_applicant": job.accepting_applicant,
        "posted_date": job.posted_date.isoformat(),
        "job_category": job.job_category.category_name if job.job_category else None,
        "user_id": job.user_id
    }
    return jsonify(result), 200


# ---------------------------
# UPDATE a Job
# ---------------------------
@job_bp.route("/job/<int:id>", methods=["PUT"])
@jwt_required()
def update_job(id):
    job = Job.query.get(id)
    if not job:
        return jsonify({"message": "Job not found"}), 404

    current_user_id = int(get_jwt_identity())
    if job.user_id != current_user_id:
        return jsonify({"message": "You are not allowed to update this job"}), 403

    data = request.get_json()
    job.title = data.get("title", job.title)
    job.description = data.get("description", job.description)
    job.active = data.get("active", job.active)
    job.accepting_applicant = data.get("accepting_applicant", job.accepting_applicant)

    job_category_id = data.get("job_category_id")
    if job_category_id:
        category = JobCategory.query.get(job_category_id)
        if not category:
            return jsonify({"message": "Invalid job category"}), 400
        job.job_category_id = job_category_id

    db.session.commit()
    return jsonify({"message": "Job updated", "job_id": job.id}), 200


# ---------------------------
# DELETE a Job
# ---------------------------
@job_bp.route("/job/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_job(id):
    job = Job.query.get(id)
    if not job:
        return jsonify({"message": "Job not found"}), 404

    current_user_id = int(get_jwt_identity())
    if job.user_id != current_user_id:
        return jsonify({"message": "You are not allowed to delete this job"}), 403

    db.session.delete(job)
    db.session.commit()
    return jsonify({"message": "Job deleted"}), 200


# @job_bp.route("/Job_Listings", methods=["POST"])
# @jwt_required
# def job_listing():
#     try:
#         {}
#     except Exception as e:
#         return {
#             "success":False,
#             "message":f"{e}"
#         }
    
# this complete job category crud is written with the help of ai
@job_bp.route("/job_category", methods=["POST"])
@jwt_required()
def create_job_category():
    data = request.json
    print(data)
    name = data.get("category_name")
    if not name:
        return jsonify({"message": "Category name is required"}), 400

    # Check if category already exists
    if JobCategory.query.filter_by(category_name=name).first():
        return jsonify({"message": "Category already exists"}), 409

    category = JobCategory(category_name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({"message": "Job category created", "id": category.id}), 201

# ---------------------------
# READ all JobCategories
# ---------------------------
@job_bp.route("/job_category", methods=["GET"])
@jwt_required()
def get_all_job_categories():
    categories = JobCategory.query.all()
    result = [{"id": c.id, "category_name": c.category_name} for c in categories]
    return jsonify(result), 200

# ---------------------------
# READ single JobCategory
# ---------------------------
@job_bp.route("/job_category/<int:id>", methods=["GET"])
@jwt_required()
def get_job_category(id):
    category = JobCategory.query.get(id)
    if not category:
        return jsonify({"message": "Job category not found"}), 404
    return jsonify({"id": category.id, "category_name": category.category_name}), 200

# ---------------------------
# UPDATE JobCategory
# ---------------------------
@job_bp.route("/job_category/<int:id>", methods=["PUT"])
@jwt_required()
def update_job_category(id):
    category = JobCategory.query.get(id)
    if not category:
        return jsonify({"message": "Job category not found"}), 404

    data = request.json
    name = data.get("category_name")
    if not name:
        return jsonify({"message": "Category name is required"}), 400

    # Optional: check duplicate
    if JobCategory.query.filter(JobCategory.category_name == name, JobCategory.id != id).first():
        return jsonify({"message": "Category name already exists"}), 409

    category.category_name = name
    db.session.commit()
    return jsonify({"message": "Job category updated", "id": category.id}), 200

# ---------------------------
# DELETE JobCategory
# ---------------------------
@job_bp.route("/job_category/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_job_category(id):
    category = JobCategory.query.get(id)
    if not category:
        return jsonify({"message": "Job category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Job category deleted"}), 200