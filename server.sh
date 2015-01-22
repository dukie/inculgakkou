#!/bin/bash

case "$1" in
"start")
uwsgi --file uwsgi.py --module uwsgi --limit-as 128 -p 5 -M --fastcgi-socket 127.0.0.1:8882 --pidfile=/tmp/inculserver.pid --daemonize /tmp/incul.log --die-on-term
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
