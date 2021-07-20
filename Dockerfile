FROM python:3.7-alpine

# SET ENVIRONMENT WITH PYTHON   
ENV PYTHONUNBUFFERED 1

# INSTALL DEPENDENCIES FOR PGSQL

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client

# INSTALL TEMPORAL DEPENDENCIES FOR THE PYTHON PACKAGES
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

# INSTALL THE REQUIREMENTS
RUN pip install -r /requirements.txt

# DELETE TEMPORAL PACKAGES 
RUN apk del .tmp-build-deps

RUN mkdir /backend_challenge
WORKDIR /app
COPY ./app /app

RUN adduser -D user
USER user
