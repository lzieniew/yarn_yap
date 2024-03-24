#Warning! This dockerfile is meant to be built with context set to top directory of this project

FROM python:3.12-slim

WORKDIR /app

# Copy the Python script into the container
COPY worker/requirements.txt /app/requirements.txt
COPY shared /app/shared

# Install pymongo for MongoDB interaction
RUN pip install -r /app/requirements.txt

COPY worker /app

CMD ["python", "worker.py"]
