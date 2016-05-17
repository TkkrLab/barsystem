from django.core.management.base import BaseCommand
from django.conf import settings
import paho.mqtt.client as mqtt

from barsystem_base.models import Token

from decimal import Decimal

def on_connect(client, userdata, flags, rc):
    # print('on_connect {} {} {}'.format( userdata, flags, rc))
    client.subscribe(settings.MQTT_TOPIC)

def on_message(client, userdata, message):
    if message.topic != settings.MQTT_TOPIC:
        return
    # print("Received message '" + str(message.payload) + "' on topic '"
    #     + message.topic + "' with QoS " + str(message.qos))
    try:
        args = message.payload.decode('ascii').split(',')
    except UnicodeDecodeError:
        return
    if len(args) < 3:
        return
    client_id, command, *args = args
    if not client_id.startswith('candymachine_'):
        return
    if command == 'rq_saldo':
        button_hash = args[0]
        # print('saldo request:', button_hash)
        try:
            token = Token.objects.get(type='sha256', value=button_hash)
            saldo = token.person.amount
            username = token.person.nick_name
        except Token.DoesNotExist:
            saldo = Decimal(0.0)
            username = None
        reply = ','.join([
            client_id,
            'rp_saldo',
            '{:.2f}'.format(saldo),
            str(username)
        ])
        client.publish(message.topic, reply)
        # print('saldo_reply: ', reply)

def on_log(client, userdata, level, buf):
    print('on_log[{}] "{}"'.format(level, buf))

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        # client.on_log = on_log
        client.connect_async(settings.MQTT_BROKER)
        try:
            client.loop_forever()
        finally:
            client.disconnect()