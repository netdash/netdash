FROM python:3.7

RUN pip install psycopg2-binary

EXPOSE 8000

RUN pip install pipenv 

RUN mkdir /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pipenv install --system

WORKDIR /usr/src/app/src/netdash

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]

# TODO add CMD with gunicorn
