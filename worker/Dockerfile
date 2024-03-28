#Warning! This dockerfile is meant to be built with context set to top directory of this project

FROM python:3.12

WORKDIR /app

COPY worker/requirements.txt /app/requirements.txt
COPY shared_components /app/shared_components

RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install watchdog

ENV PYTHONPATH /app

CMD ["watchmedo", "auto-restart", "--directory=/app", "--pattern=*.py", "--recursive", "--", "python", "/app/worker/worker.py"]
