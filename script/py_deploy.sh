#!/bin/bash

PRG="$0"
while [ -h "$PRG" ] ; do

  # shellcheck disable=SC2006
  ls=`ls -ld "$PRG"`

  # shellcheck disable=SC2006
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else

    # shellcheck disable=SC2006
    PRG=`dirname "$PRG"`/"$link"
  fi
done

# shellcheck disable=SC2164
# shellcheck disable=SC2046
PRGDIR=$(cd $(dirname "$PRG"); pwd)

# shellcheck disable=SC2164
cd $PRGDIR
cd ../

# shellcheck disable=SC2009
ps -ef | grep "python"

# shellcheck disable=SC2046
ps aux | grep [p]ython | awk '{print $2}' | xargs -I {} kill -9 {}

# install python version 3.9.1
sudo /usr/bin/pip3.9  install -r requirements.txt  --use-feature=2020-resolver  -i https://pypi.tuna.tsinghua.edu.cn/simple some-package

nohup /usr/bin/python3.9 ./manage.py runserver 127.0.0.1:8000  --noreload >> ~/log/running_ai.log 2>&1 &