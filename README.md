# barsystem

Barsystem designed for TkkrLab (www.tkkrlab.nl).

Install barsystem on a server or locally.
Install barlink on the system that runs the browser, and where the iButton reader is connected to.

## Barsystem
Barsystem is the main server, it is a django application that allows people to buy products.

To install:
* (optional, but recommended) Create a [virtualenv](https://virtualenv.pypa.io/en/stable/) and activate it.
  * Make sure you have a recent version of virtualenv (>=15.1.0).
  * Run `virtualenv -p python3 <location>`.
  * Activate the virtualenv (see virtualenv docs for how to activate on your shell).
* From the source directory, run `pip install ./barsystem`
* Run `barsystem-installer init`
* For testing, run barsystem with `django-admin runserver --settings barsystem.local_settings`
* For production, a standard nginx + uwsgi stack is recommended.
  
## Barlink
Barlink processes login tokens and product barcodes and sends these to barsystem.

It uses websockets to communicate with barsystem via the local webbrowser.
It sends data received from a serial port on to the browser, which parses and processes the data.
It works on the index page for login keys, and on the product page for barcodes.

Installation:
* See above for virtualenv
* From the source directory, run `pip install ./barlink`
* Run `barlink`
