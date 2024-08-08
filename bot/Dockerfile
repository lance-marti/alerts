# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r /app/requirements.txt

# Expose the default port used by Streamlit
EXPOSE 8501

# Run the Streamlit app when the container launches
CMD ["sh", "-c", "streamlit run src/app.py ${PORT:+--server.port=$PORT} --server.address=0.0.0.0"]