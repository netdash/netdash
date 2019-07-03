FROM python:3.7

RUN pip install psycopg2-binary
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

EXPOSE 8000
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update
RUN apt-get install -y xmlsec1 libffi-dev libssl-dev

RUN pip3 install psycopg2-binary gunicorn pipenv

RUN mkdir /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pipenv install --system --deploy

WORKDIR /usr/src/app/src/netdash

RUN chmod -R g+rw /usr/src/app

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]

CMD ["gunicorn", "--bind=0.0.0.0:8000", "netdash.wsgi"]
