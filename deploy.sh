#!/bin/bash



screen -S django -X stuff "pkill -f runserver\n"
<<<<<<< HEAD
screen -S django -X stuff "git fetch origin deployment && git reset --hard origin/deployment && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000
=======
screen -S django -X stuff "git pull origin deployment2 && git reset --hard origin/deployment2 && pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000
>>>>>>> 98f30dd1c9bab77e816ae685b8bd5629aba33eb0
\n"


