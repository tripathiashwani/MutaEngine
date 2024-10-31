#!/bin/bash

PROJECT_DIR="/path/to/backend_career_website"
VENV_PATH=" venv/bin/activate"

screen -S django -X stuff "pkill -f runserver\n"
screen -S django -X stuff "git pull origin deployment && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000\n"


# check if the pipeline is working testing pipeline test3 for the third time