FROM python:3.7

RUN pip install psycopg2-binary

EXPOSE 8000

RUN mkdir /usr/src/app

COPY . /usr/src/app

RUN pip install /usr/src/app

WORKDIR /usr/src/app/src/netdash

ENTRYPOINT ["/usr/src/app/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
