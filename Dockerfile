FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apt-get update && apt-get install -y \
#   && pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY backend /app/backend

RUN mkdir -p /app/uploads

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]