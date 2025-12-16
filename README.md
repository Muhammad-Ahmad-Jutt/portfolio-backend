# Python Flask Project

## Overview
This is a Python Flask project following best practices for project structure and development. The project structure is inspired by the tutorial https://muneebdev.com/flask-project-structure-best-practices/.

The project includes features such as custom permissions handling, date parsing utilities, database migrations and seeding, and Flask application setup with Docker.

## Project Structure
The project follows a modular structure for better maintainability:

project_root/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── seed.py
│   └── utils.py
│
├── migrations/
│
├── Dockerfile
├── docker-compose.yml
├── run.py
└── entrypoint.sh

## Notable Functions
permission_required:
def permission_required(*permission_numbers):
    """
    Custom decorator for checking user permissions.
    Function inspired by AI: https://chatgpt.com/share/6941146d-9168-8009-962b-6b790d1baf38
    """
    # Implementation goes here
create job api updated to add validations in form using this :https://chatgpt.com/share/694125a6-7db4-8009-afec-bd938c11b4bf
parse_date:
def parse_date(date_str):
    Function inspired by AI: https://chatgpt.com/share/694113bf-60b8-8009-91ad-3b503b109c3c
    """
sign up validations:https://chatgpt.com/share/6941146d-9168-8009-962b-6b790d1baf38

job category crud: https://chatgpt.com/share/69411dab-aefc-8009-98f0-e7f153d16f62

the database tables are generated with help of ai using the erd cvs export https://lucid.app/lucidchart/47b5ed82-089f-4945-9ef3-df1771af7d9f/edit?viewport_loc=360%2C-283%2C2335%2C1007%2C0_0&invitationId=inv_962072f3-c84d-4a1c-a464-5fe7b44e79de

the cv to db tables chat :https://chatgpt.com/share/694123e6-d11c-8009-a3d4-b61b9639c696

cors configration and adding comments on that file :https://chatgpt.com/share/694125a6-7db4-8009-afec-bd938c11b4bf

The project structure is inspired by the tutorial https://muneebdev.com/flask-project-structure-best-practices/.

Docker entry point file creation: https://chatgpt.com/share/69412776-8f6c-8009-8f4c-481e228f142b

Readme file creation link :https://chatgpt.com/share/69412776-8f6c-8009-8f4c-481e228f142b

## Setup and Usage

Option 1: Using Docker
1. Build and run the container:
docker-compose up --build

2. The container runs the following commands automatically on the first start:
- flask db init (if not already initialized)  
- flask db migrate  
- flask db upgrade  
- python -m app.seed  
- python run.py (starts the Flask server)  

Option 2: Running Locally with Virtual Environment
1. Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Install dependencies:
pip install -r requirements.txt

3. Set environment variables:
export FLASK_APP=run.py
export FLASK_ENV=development

4. Run database migrations:
flask db init
flask db migrate
flask db upgrade

5. Seed the database:
python -m app.seed

6. Start the Flask server:
python run.py

## License
This project is licensed under the MIT License.
