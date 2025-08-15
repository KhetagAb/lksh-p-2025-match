# !/usr/bin/bash

export $(grep -v '^#' .env | xargs)
python -m lkshmatch.tg_bot.bot