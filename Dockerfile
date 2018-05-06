FROM python:3
WORKDIR /usr/src/app

ADD . / /usr/src/app/

pip install --no-cache-dir networkx
pip install --no-cache-dir joblib

RUN ./script.sh
