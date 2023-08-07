FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt /backend/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /backend/

RUN python manage.py migrate

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]