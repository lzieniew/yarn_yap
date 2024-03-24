#Warning! This dockerfile is meant to be built with context set to top directory of this project

FROM python:3.12

WORKDIR /app

COPY shared /app/shared
COPY backend/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY backend /app/

WORKDIR /app

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--reload"]
