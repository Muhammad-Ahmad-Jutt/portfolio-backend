from . import create_app, db
from .models.user import Role, Permission, JobCategory,User
from werkzeug.security import generate_password_hash


app = create_app()
app.app_context().push()


permissions = [
    {"action":"create","resource":"job","per_no":3001},
    {"action":"update","resource":"job","per_no":3002},
    {"action":"delete","resource":"job","per_no":3003},
    {"action":"view","resource":"job","per_no":3004},
    {"action":"apply","resource":"job","per_no":3005},
    # super user permissions
    {"action":"create","resource":"job","per_no":35},
    {"action":"update","resource":"job","per_no":34},
    {"action":"delete","resource":"job","per_no":33},
    {"action":"view","resource":"job","per_no":32},
    {"action":"delete","resource":"user","per_no":31},
    {"action":"su", "resource":"app", "per_no":41},
    
]

recruiter_permissions = [3001,3002,3003,3004]
job_seeker_permissions = [3005,3004]
# super user permissions
super_user_permissions = [31,32,33,34,35]

for perm in permissions:
    per_entry = Permission.query.filter_by(action=perm['action'], resource=perm['resource'], per_no=perm['per_no']).first()
    if not per_entry:
        db.session.add(Permission(**perm))
db.session.commit()
print('permissions committed---->')

roles = ['recruiter','job_seeker', "super_user"]
for role_name in roles:
    role_entry = Role.query.filter_by(name=role_name).first()
    if not role_entry:
        db.session.add(Role(name=role_name))
db.session.commit()
print('roles committed---->')

recruiter_role = Role.query.filter_by(name='recruiter').first()
job_seeker_role = Role.query.filter_by(name='job_seeker').first()
super_user_role = Role.query.filter_by(name='super_user').first()
for permission_no in recruiter_permissions:
    perm = Permission.query.filter_by(per_no=permission_no).first()
    if perm and perm not in recruiter_role.permissions:
        recruiter_role.permissions.append(perm)

for permission_no in job_seeker_permissions:
    perm = Permission.query.filter_by(per_no=permission_no).first()
    if perm and perm not in job_seeker_role.permissions:
        job_seeker_role.permissions.append(perm)

for permission_no in super_user_permissions:
    perm = Permission.query.filter_by(per_no=permission_no).first()
    if perm and perm not in super_user_role.permissions:
        super_user_role.permissions.append(perm)

db.session.commit()
print('permissions for roles committed---->')

categories = ["IT", "Marketing", "Finance","Health"]
for cat in categories:
    category = JobCategory.query.filter_by(category_name=cat).first()
    if not category:
        db.session.add(JobCategory(category_name=cat))
db.session.commit()

admin_email = "official_recruiter@gmail.com"
if not User.query.filter_by(email=admin_email).first():
    admin_user = User(
        firstname="Recruiter",
        lastname="Admin",
        email=admin_email,
        password_hash=generate_password_hash("Admin123!"),
        recovery_email="recruiter_recovery@gmail.com",
    )
    admin_user.roles = [recruiter_role]
    db.session.add(admin_user)
    db.session.commit()
print('default user created---->')

super_user_email = "super@super.com"
if not User.query.filter_by(email=super_user_email).first():
    super_user = User(
        firstname="su",
        lastname="super",
        email=super_user_email,
        password_hash=generate_password_hash("super"),
        recovery_email="super@super.com",
    )
    super_user.roles = [super_user_role]
    db.session.add(super_user)
    db.session.commit()
print('super_user created---->')