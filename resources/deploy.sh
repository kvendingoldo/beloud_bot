#!/bin/bash

VERSION="rc-0.1.0"
TBOT_TOKEN="<TOKEN>"

docker run -d \
    --name=beloud_bot \
    --restart=always \
    -v  /home/ubuntu/tbots/data/beloud_bot:/home/tbot/bot/data \
    -e DB_URL=sqlite:////home/tbot/bot/data/beloud_bot.db \
    -e TG_BOT_TOKEN=${TBOT_TOKEN} \
    kvendingoldo/beloud_bot:${VERSION}
