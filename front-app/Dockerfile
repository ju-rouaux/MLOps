# Use a base Python image with Alpine for a smaller footprint
FROM python:3.11.11

USER root

# Set the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY /app .

# Install the required Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to access the API (changed to 8000 to match original Dockerfile)
EXPOSE 8000

# Command to run the Flask application
CMD ["python", "-u", "main.py"]