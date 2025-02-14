FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any Python dependencies
RUN conda env create -f environment.yml -n ingestion

# Make port 80 available to the world outside this container
EXPOSE 80

# When the container launches
CMD ["conda", "run", "-n", "ingestion", "python", "app/app.py"]