from django.core.management.base import BaseCommand
from django.conf import settings
import paho.mqtt.client as mqtt

from barsystem_base.models import Person, Token, VendingMachineProduct
from barsystem_base.cart import Cart

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
    process_cmd(client, message.topic, client_id, command, *args)

def process_cmd(client, topic, client_id, command, *args):
    if client_id != settings.MQTT_CLIENT_ID:
        client._easy_log(mqtt.MQTT_LOG_ERR, 'Error: invalid client_id: "{}"'.format(client_id))
        return
    if command.startswith('rp_'):
        # ignore response messages
        pass

    elif command == 'rq_code':
        if len(args) != 1:
            return
        code = args[0]
        try:
            person = Person.objects.get(active=True, member=False, id=code)
            reply = make_reply(
                client_id,
                'rp_saldo',
                '{:.2f}'.format(person.amount),
                str(person.nick_name)
            )
        except Person.DoesNotExist:
            reply = make_reply(
                client_id,
                'rp_error',
                'Invalid user'
            )
        client.publish(topic, reply)

    elif command == 'rq_saldo':
        if len(args) != 1:
            return
        button_hash = args[0]
        client._easy_log(mqtt.MQTT_LOG_INFO, 'saldo request: {}'.format(button_hash))
        try:
            token = Token.objects.get(type='sha256', value=button_hash, person__active=True)
            reply = make_reply(
                client_id,
                'rp_saldo',
                '{:.2f}'.format(token.person.amount),
                str(token.person.nick_name)
            )
        except Token.DoesNotExist:
            reply = make_reply(
                client_id,
                'rp_error',
                'Unknown iButton'
            )
        client._easy_log(mqtt.MQTT_LOG_INFO, 'saldo_reply: {}'.format(reply))
        client.publish(topic, reply)

    elif command == 'rq_vend':
        if len(args) != 2:
            client._easy_log(mqtt.MQTT_LOG_ERR, 'Error: invalid args')
            return
        try:
            button_hash, code = args
        except ValueError:
            client._easy_log(mqtt.MQTT_LOG_ERR, 'Error: Invalid args')
            return
        if button_hash.startswith('guest_'):
            guest_id = button_hash.split('_')[1]
            client.publish(
                topic,
                make_reply(client_id, 'rp_error', 'Hoi guest {}'.format(guest_id))
            )
            return
        else:
            try:
                token = Token.objects.get(type='sha256', value=button_hash, person__active=True)
            except Token.DoesNotExist:
                client.publish(
                    topic,
                    make_reply(client_id, 'rp_error', 'Unknown iButton')
                )
                return
        if token.person.special and token.person.type == 'attendant':
            if code == '99':
                client.publish(
                    topic,
                    make_reply(client_id, 'rp_passthrough')
                )
                return
        try:
            vending_product = VendingMachineProduct.objects.get(code=code)
            product = vending_product.product
        except VendingMachineProduct.DoesNotExist:
            client.publish(
                topic,
                make_reply(client_id, 'rp_error', 'Invalid code!')
            )
            return

        cart = Cart(person=token.person)
        cart.add_product(product, 1)
        success = cart.checkout()
        if not success:
            client.publish(
                topic,
                make_reply(client_id, 'rp_error', 'Transaction failed')
            )
            return

        if vending_product.virtual:
            client.publish(
                topic,
                make_reply(client_id, 'rp_error', 'OK: {}'.format(product.name))
            )
            return

        client.publish(
            topic,
            make_reply(client_id, 'rp_vend', code)
        )
        return

    elif command == 'connect':
        client.publish(topic, make_reply(
            client_id,
            'rp_setmessage',
            'Welcome, btn plz'
        ))

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
        if hasattr(settings, 'MQTT_AUTHENTICATION'):
            client.username_pw_set(*settings.MQTT_AUTHENTICATION)
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_log = on_log
        client.connect_async(settings.MQTT_BROKER)
        try:
            client.loop_forever()
        finally:
            client.disconnect()