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
    Function inspired by AI: https://chatgpt.com/c/693e49bc-8530-832b-9964-c52d31a1dcb0
    """
    # Implementation goes here

parse_date:
def parse_date(date_str):
    """
    Utility function to parse a string into a Python date object.
    Function inspired by AI: https://chatgpt.com/c/693c04a1-dbd4-832c-8a14-15e6e5ac3b2f
    """
    # Implementation goes here

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
