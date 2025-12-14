# This file will contain all the super_user api's for the super user
from flask import Blueprint,request, jsonify
from ...extensions import db
from ...models.user import  User,JobCategory,Job, JobApplication,Role
from datetime import datetime
from sqlalchemy.sql import exists
from flask_jwt_extended import jwt_required, get_jwt_identity#, current_user
from flask_login import current_user,login_required
from ..utils.decorator import permission_required
super_bp=Blueprint("super",__name__)


@super_bp.route("/view_total", methods=['GET'])
@jwt_required()
@permission_required(31,34,33,41)
def view_total():
    try:
        job = Job.query.count()
        user_accounts = User.query.count()
        job_applications = JobApplication.query.count()
        return jsonify({
            "success":True,
            "message":"Data Feched Successfull",
            "data":{
            "jobs_count":job,
            "user_registered":user_accounts,
            "applications_received":job_applications
            }
        })
    except Exception as e:
        return jsonify({
            "success":False,
            "message":str(e)[:200],
            
        })

@super_bp.route("/view_all_jobs", methods=["GET"])
@jwt_required()
@permission_required(31,34,33,41)
def get_my_job_aplications():
    jobs = Job.query.all()
    refined_jobs = []
    for job in jobs:
        current_data={}
        job_count = JobApplication.query.filter_by(job_id =job.id).count()
        current_data =   {
                "id": job.id,
                "title": job.title,
                "active":job.active,
                "active_date": str(job.active_date),
                "active_till": str(job.active_till),
                "aplication_count":job_count
                }
        refined_jobs.append(current_data)
    return jsonify({
            "success": True,
            "jobs": refined_jobs,
                })


@super_bp.route("/get_all_users", methods=["GET"])
@jwt_required()
@permission_required(31,34,33,41)
def get_all_users():
    try:

        recruiters = User.query.filter(
            User.roles.any(Role.name == "recruiter")
        ).all()

        job_seekers = User.query.filter(
            User.roles.any(Role.name == "job_seeker")
        ).all()
        def serialize_user(user):
            return {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "blocked": user.blocked,
                "roles": [role.name for role in user.roles],
                "account_created": user.account_created
            }

        return jsonify({
            "success": True,
            "message": "Users fetched successfully",
            "data": {
                "recruiters": [serialize_user(user) for user in recruiters],
                "job_seekers": [serialize_user(user) for user in job_seekers]
            },
            "counts": {
                "recruiters": len(recruiters),
                "job_seekers": len(job_seekers)
            }
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)[:200]
        }), 500
    