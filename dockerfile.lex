# Docker Container for Lexor Llamfax Service
FROM jfloff/alpine-python:latest

ARG DBHOST="LFXMongo"
ENV DBHOST=${DBHOST}
ENV BUILDVER="1.07.1822"

USER root
# -p makes dirs recursive, even if parent exists
RUN mkdir -p /llamafax/lib
# Imports App Dependancies
ADD app/lexor.py /llamafax/.
ADD app/lib/. /llamafax/lib/.

# Update and install Pip packages
RUN apk update && apk upgrade && pip3 install --upgrade pip
RUN pip3 install pymongo nltk

WORKDIR /llamafax

CMD python3 lexor.py