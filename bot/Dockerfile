# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./src/. /app

# Install any needed packages specified in requirements.txt
RUN pip install  -r /app/requirements.txt

# Expose port 8000
EXPOSE 8000

# Run count.py when the container launches
CMD ["python", "count.py"]
