# base image for the Docker image
FROM python:3.11

# Working Directory inside the container where the application code will be placed 
# WORKDIR 

# Copy the requirements.txt file from the project's working directory
COPY requirements.txt requirements.txt

# Execute a command in the Docker image
RUN pip install --no-cache-dir -r requirements.txt

# Copy the "main.py" file (and the key_comp directory)
# from the project's working directory to the Docker image's working directory
COPY /app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
