FROM python:3.11.11-alpine3.21

# Set the working directory in the container
WORKDIR /app

# Copy the app directory contents into the container
COPY /app .

# Install any Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# When the container launches
CMD ["python", "main.py"]