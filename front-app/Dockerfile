FROM bitnami/pytorch:2.6.0

USER root

# Set the working directory in the container
WORKDIR /app

# Install the required Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY /app .

# Expose port 8000 to access the API (changed to 8000 to match original Dockerfile)
EXPOSE 8000

# Command to run the Flask application
CMD ["python", "-u", "main.py"]