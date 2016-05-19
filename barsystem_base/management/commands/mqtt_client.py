from django.core.management.base import BaseCommand
from django.conf import settings
import paho.mqtt.client as mqtt

from barsystem_base.models import Token

from decimal import Decimal

def make_reply(client_id, response, *args):
    return ','.join([client_id, response] + list(args))

def on_connect(client, userdata, flags, rc):
    # print('on_connect {} {} {}'.format( userdata, flags, rc))
    client._easy_log(mqtt.MQTT_LOG_INFO, 'Connected, subscribing to topic "{}"'.format(settings.MQTT_TOPIC))
    client.subscribe(settings.MQTT_TOPIC)

def on_message(client, userdata, message):
    try:
        args = message.payload.decode('ascii').split(',')
    except UnicodeDecodeError:
        client._easy_log(mqtt.MQTT_LOG_ERR, 'Error: cannot decode payload "{}"!'.format(message.payload))
        return
    client._easy_log(mqtt.MQTT_LOG_INFO, 'args: {}'.format(args))
    if len(args) < 2:
        client._easy_log(mqtt.MQTT_LOG_ERR, 'Error: not enough args')
        return
    try:
        client_id, command, *args = args
    except ValueError:
        client._easy_log(mqtt.MQTT_LOG_ERR, 'Error unpacking args')
        return
    if client_id != settings.MQTT_CLIENT_ID:
        client._easy_log(mqtt.MQTT_LOG_ERR, 'Error: invalid client_id: "{}"'.format(client_id))
        return
    if command.startswith('rp_'):
        # ignore response messages
        pass
    elif command == 'rq_saldo':
        button_hash = args[0]
        client._easy_log(mqtt.MQTT_LOG_INFO, 'saldo request: {}'.format(button_hash))
        try:
            token = Token.objects.get(type='sha256', value=button_hash)
            reply = make_reply(
                client_id,
                'rp_saldo',
                '{:.2f}'.format(token.person.amount),
                str(token.person.nick_name)
            )
        except Token.DoesNotExist:
            reply = make_reply(client_id, 'rp_error', 'Unknown iButton')
        client._easy_log(mqtt.MQTT_LOG_INFO, 'saldo_reply: {}'.format(reply))
        client.publish(message.topic, reply)
    elif command == 'connect':
        client.publish(message.topic, ','.join([
            client_id,
            'rp_setmessage',
            'Welcome, btn plz'
        ]))
    else:
        client._easy_log(
            mqtt.MQTT_LOG_INFO,
            'Received unknown command: "{}" with args "{}"'.format(command, args)
        )

def on_log(client, userdata, level, buf):
    if userdata['verbosity'] > 1:
        print('on_log[{}] "{}"'.format(level, buf))

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        client = mqtt.Client(userdata={
            'verbosity': kwargs['verbosity']
        })
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_log = on_log
        client.connect_async(settings.MQTT_BROKER)
        try:
            client.loop_forever()
        finally:
            client.disconnect()