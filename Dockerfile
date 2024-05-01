# Use the official Python image as a base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /ecommerce

# Copy the Pipfile and Pipfile.lock to the working directory
COPY Pipfile Pipfile.lock /ecommerce/

# Install pipenv
RUN pip install --no-cache-dir pipenv

# Install dependencies
RUN pipenv install --deploy --system

# Copy the content of the local src directory to the working directory
COPY . /ecommerce/

# Expose port 5000 to the outside world
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "main.py"]

# Command to run the prepopulate script for db
CMD ["python", "prepopulate.py"]
