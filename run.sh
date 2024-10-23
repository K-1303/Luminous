#!/bin/bash

# Remove the database
rm -rf db.sqlite3

# Create database migrations
python3 manage.py makemigrations

# Apply database migrations
python3 manage.py migrate

# Create superuser non-interactively
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin')" | python3 manage.py shell

# Generate some data
python3 manage.py data_generator