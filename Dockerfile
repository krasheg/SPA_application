FROM python:3.11.2-slim-buster


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR app/

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

RUN apt-get update

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput

EXPOSE 8000
