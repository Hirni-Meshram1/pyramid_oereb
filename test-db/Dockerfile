FROM hirnimeshram/postgres-x86:12

#LABEL maintainer Camptocamp "info@camptocamp.com"

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB pyramid_oereb

COPY *.sql /docker-entrypoint-initdb.d/
