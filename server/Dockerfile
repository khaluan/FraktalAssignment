# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ../files ./files
COPY ../certs ./certs
COPY ../server ./server
COPY ../utils ./utils
COPY received.txt ./received.txt

EXPOSE 4443 5353

# Run main.py when the container launches
CMD ["python", "-m", "server.main"]