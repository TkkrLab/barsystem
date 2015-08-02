#!/bin/sh

DIR=$(dirname $(readlink -f $0))
cd $DIR

source bin/activate

trap 'kill %1' SIGINT
uwsgi \
	--chdir=$DIR \
	--plugins=python \
	--home=$DIR \
	--module=barsystem.wsgi:application \
	\
	--master \
	--vacuum \
	--socket=$DIR/server_config/socket.sock \
	--chmod=777 \
	\
	& python3 barlink/websocket.py
trap - SIGINT