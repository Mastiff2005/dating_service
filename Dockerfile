FROM python:3.8.5
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
CMD gunicorn dating_service.wsgi:application --bind 0.0.0.0:8000