FROM python:3.12-slim

WORKDIR /app

# Copy the Python script into the container
COPY worker.py /app/
COPY requirements.txt /app/

# Install pymongo for MongoDB interaction
RUN pip install -r /app/requirements.txt

CMD ["python", "worker.py"]

