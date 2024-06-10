#!/bin/bash

# Navigate to the vietan directory
cd /home/ubuntu/www/vietan || { echo "Directory not found"; exit 1; }

# Pull the latest changes from the git repository
git pull || { echo "Git pull failed"; exit 1; }

# Reload the systemd manager configuration
sudo systemctl daemon-reload || { echo "Systemctl daemon-reload failed"; exit 1; }

# Restart the Gunicorn service
sudo systemctl restart gunicorn || { echo "Systemctl restart gunicorn failed"; exit 1; }

# Restart the Nginx service
sudo service nginx restart || { echo "Nginx restart failed"; exit 1; }

echo "Update and services restarted successfully."
