FROM bitnami/spark:3.5.5

USER root

# Set the working directory in the container
WORKDIR /app

# Install any Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory contents into the container
COPY /app .

# Make port 80 available to the world outside this container
EXPOSE 80

# When the container launches
CMD ["python", "-u", "main.py"]