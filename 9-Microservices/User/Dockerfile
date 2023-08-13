FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend_user

RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt /backend_user/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /backend_user/

EXPOSE 8000