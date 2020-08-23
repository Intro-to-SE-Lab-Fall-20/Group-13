from alpine:latest

RUN apk add --no-cache python3-dev
RUN apk add --no-cache py3-pip

WORKDIR /app

copy . /app

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 5000
