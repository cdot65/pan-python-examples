# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script and .env.example into the container
COPY panorama_rules_export.py .env.example ./

# Set the entrypoint for the container
ENTRYPOINT ["python", "panorama_rules_export.py"]
