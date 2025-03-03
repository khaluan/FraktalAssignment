# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ../client ./client
COPY ../controllers ./controllers
COPY ../utils ./utils

# Run main.py when the container launches
CMD ["tail", "-f", "/dev/null"]