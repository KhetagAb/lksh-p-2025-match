# !/usr/bin/bash

export $(grep -v '^#' .env | xargs)
python -m lkshmatch.mainWebapp