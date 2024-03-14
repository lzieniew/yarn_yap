# Use the specified Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app/backend

# Copy the Python dependencies file to the container
COPY ./requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local app directory to the container
COPY ./app /app/

# Command to run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]

