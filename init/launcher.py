#!/usr/bin/python3

import os
import signal
import subprocess
import sys

def sigterm_handler(_signo, _stackframe):
	sys.exit(0)

def main(argv):
	signal.signal(signal.SIGTERM, sigterm_handler)

	os.chdir(os.path.dirname(os.path.abspath(__file__)))

	with open('bin/activate_this.py') as f:
		exec(f.read(), dict(__file__='bin/activate_this.py'))

	uwsgi = subprocess.Popen(['uwsgi', '--module=barsystem.wsgi:application', '--master', '--vacuum', '--workers=5', '--socket=server_config/socket.sock', '--chmod=777'])
	barlink = subprocess.Popen(['python', 'barlink/websocket.py'])
	try:
		uwsgi.wait()
		barlink.wait()
	finally:
		uwsgi.kill()
		barlink.kill()
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))