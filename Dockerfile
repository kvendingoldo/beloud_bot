FROM python:3-alpine

#
# Create a base UID/GID and SUID/SGID which will be used by container
#
RUN addgroup -S --gid 1000 tbot \
 && adduser -S -G tbot -u 1000 -s /bin/bash tbot \
 && mkdir -p /run/user/1000 \
 && chown -R tbot /run/user/1000 /home/tbot \
 && echo tbot:100000:65536 | tee /etc/subuid | tee /etc/subgid

ENV HOME /home/tbot
ENV USER tbot
ENV XDG_RUNTIME_DIR=/run/user/1000

RUN mkdir -p ${HOME}/bot
COPY requirements.txt ${HOME}/bot

RUN apk update \
 && apk add --virtual build-deps gcc g++ python3-dev musl-dev \
 && apk add --no-cache mariadb-dev \
 && pip3 install --upgrade pip \
 && pip3 install --no-cache-dir -r ${HOME}/bot/requirements.txt \
 && apk del build-deps gcc g++

USER tbot
COPY ./src ${HOME}/bot/src
COPY ./resources ${HOME}/bot/resources

WORKDIR ${HOME}/bot/src
ENTRYPOINT ["python3", "main.py"]
