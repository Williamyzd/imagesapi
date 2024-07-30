FROM python:3.9.12-slim-buster
RUN  mkdir -p /app/log
COPY . /app
WORKDIR /app
RUN cd /app && pip install -r /app/requirements.txt
CMD gunicorn -c gun.py app:app