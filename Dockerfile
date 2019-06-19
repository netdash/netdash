FROM python:3.7

EXPOSE 8000

RUN pip install pipenv 

RUN mkdir /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pipenv install --system

RUN pip install psycopg2-binary

RUN pip install .

WORKDIR /usr/src/app/src/netdash

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
