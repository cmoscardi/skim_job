FROM continuumio/miniconda

RUN mkdir /app
WORKDIR /app

ADD . / /app/

RUN conda install -y networkx
RUN conda install -y dask

RUN ./script.sh
