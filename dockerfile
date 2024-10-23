# Base image for the backend (Django)
FROM python:3.11.9-slim-bookworm as backend

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the working directory
COPY . .

RUN chmod +x ./run.sh

RUN ./run.sh

# Expose the port that Django runs on
EXPOSE 8000

# Set the command to run when the container starts
CMD ["python", "manage.py", "runserver"]