FROM python:3.7-slim

RUN pip install psycopg2-binary
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

EXPOSE 8000
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN pip3 install psycopg2-binary gunicorn pipenv

RUN mkdir /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pipenv install --system --deploy

WORKDIR /usr/src/app/src/netdash

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=2", "--threads=4", "--access-logfile=-", "--log-file=-", "netdash.wsgi"]
