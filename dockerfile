# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.py /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.py

# Copy the entire project into the container
COPY . /app

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 (or your desired port)
EXPOSE 8000

# Command to start Django server (or use Gunicorn for production)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.wsgi:application"]
