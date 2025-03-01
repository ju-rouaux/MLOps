# Use a base image with Miniconda, spacy could not be installed using pip in the previous Dockerfile on ARM architecture
FROM continuumio/miniconda3

# Create a conda environment and install dependencies
RUN conda create -n env python=3.9
RUN conda install -n env -c conda-forge spacy flask mlflow scikit-learn gensim joblib numpy

# Define the working directory in the container
WORKDIR /app

# Copy the project files into the container
COPY /app .

# Activate the environment
SHELL ["conda", "run", "-n", "env", "/bin/bash", "-c"]

# Expose port 8000 to access the API
EXPOSE 8000

# Command to launch the Flask application
CMD ["conda", "run", "-n", "env", "python", "main.py"]
