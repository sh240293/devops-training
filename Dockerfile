# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose port for Django
EXPOSE 8000

# Run the Django development server (change if using Gunicorn for prod)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
