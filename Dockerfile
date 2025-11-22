FROM python:3.9-slim-bullseye


RUN python -m pip install --upgrade pip \
    && mkdir -p /app

WORKDIR /app

RUN pip install flask
RUN pip install flask-limiter
RUN pip install flask-session
RUN pip install requests
RUN pip install gunicorn
RUN pip install markupsafe
RUN pip install Flask-CORS

# Cài supervisor
RUN apt-get update && apt-get install -y supervisor

COPY . .

COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000 5001

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
