from alpine:latest

RUN apk add --no-cache python3-dev
RUN apk add --no-cache py3-pip

EXPOSE 5000
