FROM postgres:17.4

RUN apt-get update && apt-get install -y --no-install-recommends \
  postgresql-17-pgaudit

COPY ./1.sql /docker-entrypoint-initdb.d/
COPY ./2.sql /docker-entrypoint-initdb.d/
COPY ./3.sql /docker-entrypoint-initdb.d/