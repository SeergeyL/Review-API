FROM python:3.9

RUN mkdir /app
WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt
RUN python manage.py migrate

CMD python manage.py runserver 0:8000