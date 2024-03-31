FROM python:3.12

WORKDIR /app

COPY text_to_speech/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

