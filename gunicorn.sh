#!/bin/bash

echo "Starting gunicorn.sh script"
cd /var/lib/jenkins/workspace/career_backend
source venv/bin/activate

echo "Current Directory: $PWD"
echo "Starting migrations..." 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input
echo "Migrations and static files collection done."

# Copy Gunicorn service and socket files to systemd
sudo cp -rf gunicorn.socket /etc/systemd/system/
sudo cp -rf gunicorn.service /etc/systemd/system/

# Reload systemd to recognize new services
sudo systemctl daemon-reload

# Start Gunicorn socket
sudo systemctl start gunicorn.socket
echo "Gunicorn socket started."

# Enable and start Gunicorn service
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
echo "Gunicorn service started and enabled."

# Restart Gunicorn service to ensure changes are applied
sudo systemctl restart gunicorn

# Confirm Gunicorn status
sudo systemctl status gunicorn
