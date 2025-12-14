#!/bin/sh
set -e  # exit if any cmmand file 

flask db init || true    #if it run second time ignre error
flask db migrate
flask db upgrade

# Seed the database
python -m app.seed

# Start the server
python run.py
