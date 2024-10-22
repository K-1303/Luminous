rm -rf db.sqlite3 # Remove the database
python3 manage.py makemigrations # Create database migrations
python3 manage.py migrate # Apply database migrations
python3 manage.py createsuperuser # Create superuser
python3 manage.py data_generator  # Generate some data
# python3 manage.py runserver -> Run the server
