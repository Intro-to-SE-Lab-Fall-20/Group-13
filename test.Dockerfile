#loads the docker image
FROM alpine:latest

# Runs to add Python3 and Pip3
RUN apk add --no-cache python3
RUN apk add cmd:pip3
#RUN apk add --no-cache mariadb mariadb-client mariadb-server-utils pwgen && \
#    rm -f /var/cache/apk/*

#set work directory and copies files from current folder
WORKDIR /app
COPY . /app

#uses pip to install packages in requirments.txt
RUN pip3 --no-cache-dir install -r requirements.txt

#add environment variables to  container
RUN export FLASK_APP=app.py
RUN export FLASK_ENV=development


#exposes public port
EXPOSE 5000
STOPSIGNAL SIGINT
#sets entrypoint for application
ENTRYPOINT ["python3"]
CMD ["test"]
