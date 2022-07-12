# Docker Container for Lexor Llamfax Service
# sudo docker build -f dockerfile.lex -t jimurrito/lfxlexor:latest .

# [Notes]
# No need for persisnat storage

FROM jfloff/alpine-python:latest

USER root
# -p makes dirs recursive, even if parent exists
RUN mkdir -p /llamafax/lib
# Imports App Dependancies
ADD app/lexor.py /llamafax/.
ADD app/lib/General.py /llamafax/lib/.

# Update and install Pip packages
RUN apk update && apk upgrade && pip3 install --upgrade pip
RUN pip3 install pymongo nltk

WORKDIR /llamafax

CMD python3 lexor.py