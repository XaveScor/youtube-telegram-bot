FROM python:3.10.4-alpine3.15

WORKDIR /app

COPY requirements.txt requirements.txt
RUN apk update &&\
    apk add --no-cache --virtual .build-deps build-base &&\
    apk add --no-cache ffmpeg &&\
    pip3 install -r requirements.txt && \
    apk del .build-deps

COPY main.py main.py

CMD [ "python3", "/app/main.py"]
