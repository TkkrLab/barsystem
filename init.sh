#!/bin/bash

DIR=$(dirname $(readlink -f $0))
cd $DIR

if [[ ! -e "$DIR/bin/activate" ]]; then
	echo "Creating virtualenv"
	virtualenv3 . || virtualenv-3.4 . || exit -1
fi

echo "Activating virtualenv"
source bin/activate || exit -2

echo "Installing requirements"
pip install -r requirements.txt || exit -3

if [[ ! -x "$DIR/manage.py" ]]; then
	echo "Generating default config"
	django-admin startproject --template=init --name=nginx_params barsystem . || exit -4
fi

echo "Creating database and static dir"
./manage.py migrate
./manage.py collectstatic --noinput
./manage.py compilemessages

NGINX_CONF_PATH=`nginx -V 2>&1 | grep -e "--prefix=" | tr ' ' '\n' | grep "^--prefix=" | awk -F= '{print $2}'`

if [[ -z $NGINX_CONF_PATH ]]; then
	NGINX_CONF_PATH="/usr/local/nginx/conf"
	if [[ ! -d $NGINX_CONF_PATH ]]; then
		echo "Cannot detect nginx config path!"
		exit -5
	fi
fi

echo "Linking server config to $NGINX_CONF_PATH/barsystem.conf"
sudo ln -s $DIR/server_config/nginx_params $NGINX_CONF_PATH/barsystem_params

echo "Just add \"include barsystem_params\" in a \"server { }\" block to $NGINX_CONF_PATH/nginx.conf and restart nginx."
echo "After that launch launcher.sh (preferably on boot), and the bar should run."