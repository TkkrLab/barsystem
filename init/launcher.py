#!/usr/bin/python3

import os
import subprocess

def main(argv):
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
	import sys
	sys.exit(main(sys.argv))