# docker_tutorial/backend/Dockerfile

FROM python:3.11

# ENV PYTHONUNBUFFERED 1

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD ["python", "manage.py", "runserver"]
