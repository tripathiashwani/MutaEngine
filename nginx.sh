#!/bin/bash

# Copy app.conf to the correct Nginx sites-available directory
sudo cp -rf app.conf /etc/nginx/sites-available/app

# Set permissions on Jenkins workspace
chmod 710 /var/lib/jenkins/workspace/career_backend

# Remove any existing symbolic link and create a new one
sudo rm /etc/nginx/sites-enabled/app
sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled/

# Test Nginx configuration and reload if successful
sudo nginx -t && sudo systemctl reload nginx

# Start and enable Nginx to start on boot
sudo systemctl start nginx
sudo systemctl enable nginx

# Output status to confirm Nginx is running
echo "Nginx has been started"
sudo systemctl status nginx
