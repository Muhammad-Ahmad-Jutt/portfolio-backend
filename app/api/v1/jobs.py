# this file will handle the login and signup 

from flask import Blueprint,request, jsonify
from werkzeug.exceptions import BadRequest, BadRequestKeyError
from ...extensions import db
from ...models.user import Role, User,JobCategory,Job, JobApplication
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity#, current_user
from flask_login import current_user,login_required
job_bp=Blueprint("jobs",__name__)




job_bp = Blueprint("jobs", __name__)

# this function is ai generated 
def parse_date(date_str): # https://chatgpt.com/c/693c04a1-dbd4-832c-8a14-15e6e5ac3b2f
    """Safely parse YYYY-MM-DD date strings."""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return "invalid"


@job_bp.route("/job/applied", methods=['GET'])
@jwt_required()
def applied_jobs():
    try:
        current_user_id = int(get_jwt_identity())
        applications = JobApplication.query.filter_by(applicant_user_id=current_user_id).all()
        print(applications)
        result = []
        for job in applications:
            result.append({
                "id": job.job_id,
                "title": job.job.title,
                # "description": job.description,
                # "active": job.active,
                # "accepting_applicant": job.accepting_applicant,
                "posted_date": job.job.posted_date.isoformat(),
                "job_category": job.job.job_category.category_name if job.job.job_category else None,
                # "user_id": job.user_id,
                "application_status":job.application_status
            })
        return jsonify(result), 200

                # return jsonify({"success":True, "message":"Jo Applied successfully"})
    except Exception as e:
        return jsonify({"success":False,"message": f"An exception occured -->'{e}'"}), 404

@job_bp.route("/job/applicaton/<int:job_id>", methods=['GET'])
@jwt_required()
def applied_job_details(job_id):
    try:

        current_user_id = int(get_jwt_identity())
        application = JobApplication.query.filter_by(applicant_user_id=current_user_id,job_id=job_id).first()
        result = {
            # "id": application..id,
            "title": application.job.title,
            "description": application.job.description,
            "active": application.job.active,
            "accepting_applicant": application.job.accepting_applicant,
            "posted_date": application.job.posted_date.isoformat(),
            "job_category": application.job.job_category.category_name if application.job.job_category else None,
            "user": f"{application.job.user.firstname} {application.job.user.lastname}",
            "application_status":application.application_status,
            "applied_date":application.applied_date
            # "employer_user_id":user.id
        }
        return jsonify(result), 200


                # return jsonify({"success":True, "message":"Jo Applied successfully"})
    except Exception as e:
        return jsonify({"success":False,"message": f"An exception occured -->'{e}'"}), 404
@job_bp.route("/job/view_job_details/<int:job_id>", methods=['GET'])
@jwt_required()
def view_job_details(job_id):
    try:

        job = JobApplication.query.get(job_id)
        result = {
            # "id": application..id,
            "title": job.title,
            "description": job.description,
            "active": job.active,
            "accepting_applicant": job.accepting_applicant,
            "posted_date": job.posted_date.isoformat(),
            "job_category": job.job_category.category_name if job.job_category else None,
            "user": f"{job.user.firstname} {job.user.lastname}",
            # "application_status":application_status,
            # "applied_date":application.applied_date
            # "employer_user_id":user.id
        }
        return jsonify(result), 200


                # return jsonify({"success":True, "message":"Jo Applied successfully"})
    except Exception as e:
        return jsonify({"success":False,"message": f"An exception occured -->'{e}'"}), 404












# ---------------------------
# CREATE a Job
# ---------------------------

@job_bp.route("/job", methods=["POST"])
@jwt_required()  
def create_job():
    try:
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        active_date_str = data.get("active_date")
        active_till_str = data.get("active_till")
        job_category_id = data.get("job_category_id")
        active_status  =data.get('active')
        accepting_applicatants = data.get('accepting_applicant')
        company = data.get("company")
        if not all([title, description, active_date_str, active_till_str, job_category_id, company, active_status, accepting_applicatants]):
            return jsonify({"success": False, "error": "Missing required fields"}), 400


        # Convert string to Python date
        try:
            active_date = datetime.strptime(active_date_str, "%Y-%m-%d").date()
            active_till = datetime.strptime(active_till_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"success":False,"error": "Dates must be in YYYY-MM-DD format"}), 400

        # Ensure job category exists
        job_category = JobCategory.query.get(job_category_id)
        if not job_category:
            return jsonify({"success":False,"error": "Job category not found"}), 404

        existing_job = Job.query.filter_by(
            title=title,
            description=description,
            active_date=active_date,
            active_till=active_till,
            job_category_id=job_category_id,
            user_id=current_user.id,
            company=company,
            active=active_status,
            accepting_applicant=accepting_applicatants,
        ).first()
        if existing_job:
            return jsonify({"success":False,"error": "Job Already exist"}), 409
        job = Job(
            title=title,
            description=description,
            active_date=active_date,
            active_till=active_till,
            job_category_id=job_category_id,
            user_id=current_user.id,
            company=company,
            active=active_status,
            accepting_applicant=accepting_applicatants,
        )

        db.session.add(job)
        db.session.commit()

        return jsonify({
            "success":True,
            "message": "Job created successfully",
            "job": {
                "id": job.id,
                "title": job.title,
                "description": job.description,
                "active_date": str(job.active_date),
                "active_till": str(job.active_till),
                "job_category_id": job.job_category_id,
                "user_id": job.user_id,
                "company":company,
                "active":active_status,
                "accepting_applicant":accepting_applicatants,
            }
        }), 201
    except Exception as e:
        return jsonify({"success":False, "message":f"{e}"}),400

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
        return jsonify({"success":False,"message": "Job not found"}), 404

    user = User.query.filter_by(id=job.user_id).first()
    result = {
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "company":job.company,
        "active": job.active,
        "accepting_applicant": job.accepting_applicant,
        "posted_date": job.posted_date.isoformat(),
        "job_category": job.job_category.category_name if job.job_category else None,
        "user": f"{user.firstname} {user.lastname}",
        "employer_user_id":user.id
    }
    return jsonify(result), 200



# read jobs specific to recruters
@job_bp.route("/job/jobs_recruiters", methods=["GET"])
@jwt_required()
def get_my_jobs():
    recruiter_id = current_user.id
    jobs = Job.query.filter_by(user_id=recruiter_id).all()


    return jsonify({
            "success": True,
            "jobs": [
                {
                "id": j.id,
                "title": j.title,
                "company": j.company,
                "active_date": str(j.active_date),
                "active_till": str(j.active_till),
                "job_category_id": j.job_category_id,
                }
                for j in jobs
                ],
                })
# get only active jobs
@job_bp.route("/job/jobs_active", methods=["GET"])
@jwt_required()
def get_my_active_jobs():
    recruiter_id = current_user.id
    jobs = Job.query.filter_by(user_id=recruiter_id, active=True).all()


    return jsonify({
            "success": True,
            "jobs": [
                {
                "id": j.id,
                "title": j.title,
                "company": j.company,
                "active_date": str(j.active_date),
                "active_till": str(j.active_till),
                "job_category_id": j.job_category_id,
                }
                for j in jobs
                ],
                })

# ---------------------------
# UPDATE a Job
# ---------------------------
@job_bp.route("/job/<int:id>", methods=["PUT"])
@jwt_required()
def update_job(id):
    job = Job.query.get(id)
    if not job:
        return jsonify({"success":False,"message": "Job not found"}), 404

    current_user_id = int(get_jwt_identity())
    if job.user_id != current_user_id:
        return jsonify({"success":False,"message": "You are not allowed to update this job"}), 403

    data = request.get_json()
    

    # Update all fields from frontend if provided
    job.title = data.get("title", job.title)
    job.description = data.get("description", job.description)
    job.company = data.get("company", job.company)
    job.active_date = data.get("active_date", job.active_date)
    job.active_till = data.get("active_till", job.active_till)
    job.active = data.get("active", job.active)
    job.accepting_applicant = data.get("accepting_applicant", job.accepting_applicant)

    # Handle active_date and active_till
    active_date_str = data.get("active_date")
    active_till_str = data.get("active_till")

    active_date = parse_date(active_date_str)
    active_till = parse_date(active_till_str)

    # Handle invalid date formats
    if active_date == "invalid" or active_till == "invalid":
        return jsonify({
            "success": False,
            "error": "Dates must be in YYYY-MM-DD format"
        }), 400

    # Only update if provided
    if active_date is not None:
        job.active_date = active_date

    if active_till is not None:
        job.active_till = active_till


    # Update job category if provided
    job_category_id = data.get("job_category_id")
    if job_category_id:
        category = JobCategory.query.get(job_category_id)
        if not category:
            return jsonify({"success": False, "message": "Invalid job category"}), 400
        job.job_category_id = job_category_id

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Job updated successfully",
        "job": {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "company": job.company,
            "active_date": job.active_date.isoformat() if job.active_date else None,
            "active_till": job.active_till.isoformat() if job.active_till else None,
            "active": job.active,
            "accepting_applicant": job.accepting_applicant,
            "job_category_id": job.job_category_id,
            "job_category": job.job_category.category_name if job.job_category else None
        }
    }), 200


@job_bp.route("/job/apply", methods=['POST'])
@jwt_required()
def apply_job():
    data = request.json
    id = data.get("job_id")
    if not id:

        return ({"success":False, "message":"Id is required"})
    try:
        job_id = Job.query.filter_by(id=id).first()
        if not job_id:
            return jsonify({"success":False,"message": "Job not found"}), 404

        current_user_id = int(get_jwt_identity())
        existing = JobApplication.query.filter_by(
                        job_id=job_id.id,
                        employer_user_id=job_id.user_id,
                        applicant_user_id=current_user_id
                    ).first()

        if existing:
            return jsonify({"success": False, "message": "You have already applied to this job."}), 400


        job_application = JobApplication(employer_user_id=job_id.user_id,
                                         applicant_user_id=current_user_id,
                                         job_id=job_id.id)
        db.session.add(job_application)
        db.session.commit()
        return jsonify({"success":True, "message":"Jo Applied successfully"})
    except Exception as e:
        return jsonify({"success":False,"message": f"An exception occured -->'{e}'"}), 404



# ---------------------------
# DELETE a Job
# ---------------------------
@job_bp.route("/job/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_job(id):
    if not id:
        return ({"success":False, "message":"Id is required"})
    job = Job.query.get(id)
    if not job:
        return jsonify({"success":False,"message": "Job not found"}), 404

    current_user_id = int(get_jwt_identity())
    if job.user_id != current_user_id:
        return jsonify({"success":False,"message": "You are not allowed to delete this job"}), 403

    db.session.delete(job)
    db.session.commit()
    return jsonify({"success":True,"message": "Job deleted"}), 200


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
        return jsonify({"success":False,"message": "Category name is required"}), 400

    # Check if category already exists
    if JobCategory.query.filter_by(category_name=name).first():
        return jsonify({"success":False,"message": "Category already exists"}), 409

    category = JobCategory(category_name=name)
    db.session.add(category)
    db.session.commit()

    return jsonify({"success":True,"message": "Job category created", "id": category.id}), 201

# ---------------------------
# READ all JobCategories
# ---------------------------
@job_bp.route("/job_category", methods=["GET"])
def get_all_job_categories():
    try:
        categories = JobCategory.query.all()
        result = [{"id": c.id, "category_name": c.category_name} for c in categories]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"success":False, "message":e})
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
        return jsonify({"success":False,"message": "Job category not found"}), 404

    data = request.json
    name = data.get("category_name")
    if not name:
        return jsonify({"success":False,"message": "Category name is required"}), 400

    # Optional: check duplicate
    if JobCategory.query.filter(JobCategory.category_name == name, JobCategory.id != id).first():
        return jsonify({"success":False,"message": "Category name already exists"}), 409

    category.category_name = name
    db.session.commit()
    return jsonify({"success":True,"message": "Job category updated", "id": category.id}), 200

# ---------------------------
# DELETE JobCategory
# ---------------------------
@job_bp.route("/job_category/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_job_category(id):
    category = JobCategory.query.get(id)
    if not category:
        return jsonify({"success":False,"message": "Job category not found"}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({"success":True,"message": "Job category deleted"}), 200