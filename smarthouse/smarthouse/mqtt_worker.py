import paho.mqtt.client as mqtt
from device.models import Device
import logging
from . import config_mqtt

log = logging.getLogger(__name__)

MQTT_CONNECTION_TTL = 10


def mqtt_device_load(device_id, state):
    device = Device.objects.get(unique_id=device_id)
    device.state = state
    device.save()


def on_message(connect, userdata, message):
    device_id, state = message.payload.decode('utf-8').split(',')
    mqtt_device_load(device_id, state)
    log.info(f'От устройства {device_id} пришёл статус {state}')
    print(device_id, state)


client = mqtt.Client(config_mqtt.CLIENT_NAME)
client.on_message = on_message


def mqtt_publish(*args, **kwargs):
    if not client.is_connected():
        client.connect(config_mqtt.SERVER, keepalive=MQTT_CONNECTION_TTL)
    client.publish(*args, **kwargs)


def server_connect(connect, *args, **kwargs):
    connect.subscribe(config_mqtt.UID)


def listener():
    client.connect(config_mqtt.SERVER, keepalive=MQTT_CONNECTION_TTL)
    client.on_connect = server_connect
    client.loop_forever()
