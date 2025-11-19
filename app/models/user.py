from flask_authorize import PermissionsMixin, RestrictionsMixin, AllowancesMixin
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from ..extensions import db
# db = SQLAlchemy()
# asociation tables 
role_permission = db.Table(
    "role_permission",
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id"), primary_key=True)
)

user_role = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True)
)
user_group = db.Table(
    "user_group",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"), primary_key=True)
)

class Role(db.Model, RestrictionsMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    permissions = db.relationship("Permission", secondary=role_permission, backref="roles")

class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(50), nullable=False)
    resource = db.Column(db.String(100), nullable=False)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class User(db.Model, UserMixin, AllowancesMixin):
    __tablename__ = "users"
    __group_model__ = Group
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    emp_status = db.Column(db.String(50))
    gender = db.Column(db.String(1))
    dob = db.Column(db.Date)
    account_created = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_no = db.Column(db.String(20))
    recovery_email = db.Column(db.String(255), nullable=False)
    work_email = db.Column(db.String(255))
    roles = db.relationship("Role", secondary=user_role, backref="users")
    groups = db.relationship("Group", secondary=user_group, backref="users")

class JobCategory(db.Model):
    __tablename__ = "job_category"
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

class Job(db.Model, PermissionsMixin):
    __tablename__ = "job"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=True)
    accepting_applicant = db.Column(db.Boolean, default=True)
    posted_date = db.Column(db.Date, default=datetime.utcnow)
    active_date = db.Column(db.Date)
    active_till = db.Column(db.Date)
    reactivated_date = db.Column(db.Date)
    job_category_id = db.Column(db.Integer, db.ForeignKey("job_category.id"))
    user = db.relationship("User")
    job_category = db.relationship("JobCategory")

class JobSalary(db.Model):
    __tablename__ = "job_salary"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    min_salary = db.Column(db.Numeric(18, 2))
    max_salary = db.Column(db.Numeric(18, 2))
    negotiable = db.Column(db.Boolean, default=True)
    job = db.relationship("Job")

class JobBatch(db.Model):
    __tablename__ = "job_batch"
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    batch_no = db.Column(db.Integer)
    no_of_applicants = db.Column(db.Integer, default=0)
    max_batch_count = db.Column(db.Integer, default=1)
    max_applicant_in_batch = db.Column(db.Integer, default=1)
    job = db.relationship("Job")
    user = db.relationship("User")

class JobApplication(db.Model):
    __tablename__ = "job_application"
    job_id = db.Column(db.Integer, db.ForeignKey("job.id"), primary_key=True)
    employer_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    applicant_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    batch_id = db.Column(db.Integer, db.ForeignKey("job_batch.id"))
    application_status = db.Column(db.String(50), default="Pending")
    applied_date = db.Column(db.Date, default=datetime.utcnow)
    last_update = db.Column(db.Date, default=datetime.utcnow)
    job = db.relationship("Job")
    employer = db.relationship("User", foreign_keys=[employer_user_id])
    applicant = db.relationship("User", foreign_keys=[applicant_user_id])
    batch = db.relationship("JobBatch")
