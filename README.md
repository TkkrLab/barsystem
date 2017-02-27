barsystem
=========
Barsystem designed for TkkrLab (www.tkkrlab.nl).

Install barsystem on a server or locally.
Install barlink on the system that runs the browser, and where the iButton reader is connected to.

To install:
* (optional, but recommended) Create a [virtualenv](https://virtualenv.pypa.io/en/stable/) and activate it.
  * Make sure you have a recent version of virtualenv (>=15.1.0).
  * Run `virtualenv -p python3 <location>`.
  * Activate the virtualenv (see virtualenv docs for how to activate on your shell).
* Run `pip install barsystem` or `pip install barlink`
  * barlink can now be run with `barlink`
  * ~~For barsystem, run `barsystem-installer`~~ (not working yet)
  * Put some data in ~/.config/barsystem/secret.txt (e.g. changeme)
  * For testing, run barsystem with `django-admin runserver --settings barsystem.local_settings