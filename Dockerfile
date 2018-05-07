FROM python:3
WORKDIR /usr/src/app

ADD . / /usr/src/app/

RUN pip install --no-cache-dir networkx
RUN pip install --no-cache-dir dask

RUN ./script.sh
