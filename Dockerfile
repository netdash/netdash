FROM python:3.7

EXPOSE 8000

RUN pipenv run pip install pipenv psycopg2-binary

RUN mkdir /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pipenv install

WORKDIR /usr/src/app/src/netdash

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
