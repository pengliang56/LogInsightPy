#!/bin/bash

# shellcheck disable=SC2009
ps -ef | grep "python"

# shellcheck disable=SC2164
cd /root/LogInsightPy

git pull orign main

# shellcheck disable=SC2164
cd ~

# shellcheck disable=SC2046
[[ -f run.pid ]] && kill $(cat run.pid) && rm ~/run.pid

nohup python ~/LogInsightPy/script/manage.py runserver 127.0.0.1:8000 \
  > ~/log/app_py_01.log 2>&1 & echo $! > ~/run.pid