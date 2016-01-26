#!/bin/bash

DIR=$(dirname $(readlink -f $0))
cd $DIR

if [[ ! -e "$DIR/bin/activate" ]]; then
	echo "Creating virtualenv"
	virtualenv -p python3 . || exit -1
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
echo "Creating superuser"
./manage.py createsuperuser

NGINX_CONF_PATH=`nginx -V 2>&1 | grep -e "--prefix=" | tr ' ' '\n' | grep "^--prefix=" | awk -F= '{print $2}'`

if [[ -z $NGINX_CONF_PATH ]]; then
	NGINX_CONF_PATH="/usr/local/nginx/conf"
	if [[ ! -d $NGINX_CONF_PATH ]]; then
		echo "Cannot detect nginx config path!"
		exit -5
	fi
fi

if [[ ! -e $NGINX_CONF_PATH/barsystem_params ]]; then
	echo "Linking server config to $NGINX_CONF_PATH/barsystem.conf"
	sudo ln -s $DIR/server_config/nginx_params $NGINX_CONF_PATH/barsystem_params
fi
echo "Just add \"include barsystem_params\" in a \"server { }\" block to $NGINX_CONF_PATH/nginx.conf and restart nginx."
# echo "After that launch launcher.sh (preferably on boot), and the bar should run."

# http://unix.stackexchange.com/questions/18209/detect-init-system-using-the-shell/164092#164092
if [[ `systemctl` =~ -\.mount ]]; then
	# systemd
	echo "Assuming systemd, creating unit, enabling and starting barsystem for \"$USER\""
	(
	cat <<EOF
[Unit]
Description=Barsystem

[Service]
Type=simple
ExecStart=$DIR/launcher.py
ExecStop=
EOF
) > $HOME/.config/systemd/user/barsystem.service
	systemctl --user daemon-reload
	systemctl --user enable barsystem
	systemctl --user start barsystem
	# sudo ln -s $DIR/init.systemd /usr/lib/systemd/system/barsystem@.service
	# sudo systemctl enable barsystem@$USER
	# sudo systemctl start barsystem@$USER
elif [[ `/sbin/init --version` =~ upstart ]]; then
	# upstart
	echo "Assuming upstart, not implemented currently."
	CONFIG=$(cat <<EOF1
description     "Barsystem"
author          "Jasper Seidel <jawsper@jawsper.nl>"

# no start option as you might not want it to auto-start
# This might not be supported - you might need a: start on runlevel [3]
start on runlevel [2345]

# if you want it to automatically restart if it crashes, leave the next line in
respawn

script
    su -c $DIR/launcher.py $USER
end script
EOF1
	)
elif [[ -f /etc/init.d/cron && ! -h /etc/init.d/cron ]]; then
	# sysv
	echo "Assuming SysV, not implemented currently."

	# TODO: needs dollar escaping
	CONFIG=$(cat <<EOF2
#!/bin/sh

### BEGIN INIT INFO
# Provides:          barsystem
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Put a short description of the service here
# Description:       Put a long description of the service here
### END INIT INFO

# Change the next 3 lines to suit where you install your script and what you want to call it
DIR={{project_directory}}
USER={{user}}

DAEMON=$DIR/launcher.py
DAEMON_NAME=barsystem

# Add any command line options for your daemon here
DAEMON_OPTS=""

# This next line determines what user the script runs as.
DAEMON_USER=$USER

# The process ID of the script when it runs is stored here:
PIDFILE=/var/run/$DAEMON_NAME.pid

. /lib/lsb/init-functions

do_start () {
    log_daemon_msg "Starting system $DAEMON_NAME daemon"
    start-stop-daemon --start --background --pidfile $PIDFILE --make-pidfile --user $DAEMON_USER --chuid $DAEMON_USER --startas $DAEMON -- $DAEMON_OPTS
    log_end_msg $?
}
do_stop () {
    log_daemon_msg "Stopping system $DAEMON_NAME daemon"
    start-stop-daemon --stop --pidfile $PIDFILE --retry 10
    log_end_msg $?
}

case "$1" in

    start|stop)
        do_${1}
        ;;

    restart|reload|force-reload)
        do_stop
        do_start
        ;;

    status)
        status_of_proc "$DAEMON_NAME" "$DAEMON" && exit 0 || exit $?
        ;;

    *)
        echo "Usage: /etc/init.d/$DAEMON_NAME {start|stop|restart|status}"
        exit 1
        ;;

esac
exit 0
EOF2
)
else
	echo "Cannot determine init system in use."
fi