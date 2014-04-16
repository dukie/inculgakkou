#!/bin/bash

case "$1" in
"start")
python manage.py runfcgi method=prefork host=127.0.0.1 port=8882 pidfile=/tmp/inculserver.pid errlog=/tmp/inculerr.log outlog=/tmp/inculout.log
;;
"stop")
kill -9 `cat /tmp/inculserver.pid`
;;
"restart")
$0 stop
sleep 1
$0 start
;;
*) echo "Usage: ./server.sh {start|stop|restart}";;
esac
