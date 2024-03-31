FROM python:3.12

WORKDIR /app

COPY text_to_speech/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY shared_components /app/shared_components
RUN pip install /app/shared_components

CMD ["uvicorn", "text_to_speech.app.main:app", "--host", "0.0.0.0", "--reload"]

