from barsystem.settings import *  # NOQA
import os


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = open(os.path.expanduser('~/.config/barsystem/secret.txt')).read()


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']


# Email settings
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True
EMAIL_TARGET = ['']

# MQTT notification settings
MQTT_BROKER = ''
MQTT_AUTHENTICATION = ('', '')
MQTT_TOPIC = ''
MQTT_ALLOWED_CLIENTS = ('',)
VENDING_MACHINE_WELCOME_MESSAGE = ''
