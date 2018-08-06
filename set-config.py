import sys
from is_wire.core import Channel, Subscription, Message, Logger
from is_wire.core.wire.status import StatusCode
from is_msgs.camera_pb2 import CameraConfig
from google.protobuf.json_format import Parse

# necessery to create a CameraConfig message
from google.protobuf.wrappers_pb2 import FloatValue
from is_msgs.common_pb2 import SamplingSettings
from is_msgs.image_pb2 import ImageSettings, Resolution, ColorSpace, ColorSpaces

uri = 'amqp://10.10.2.15:30000'
channel = Channel(uri)
subscription = Subscription(channel)
log = Logger(name='SetConfig')
camera_id = 0

""" 
    Loading CameraConfig protobuf from a json file
"""
with open('camera_config.json', 'r') as f:
    try:
        set_config = Parse(f.read(), CameraConfig())
        log.info('CameraConfig:\n{}', set_config)
    except Exception as ex:
        log.critical('Unable to camera settings. \n{}', ex)
"""
    Another way to create a CameraConfig message
"""
set_config = CameraConfig(
    sampling=SamplingSettings(
        frequency=FloatValue(value=5.0)
    ),
    image=ImageSettings(
        resolution=Resolution(width=720, height=540),
        color_space=ColorSpace(value=ColorSpaces.Value('GRAY'))
    )
)

msg = Message()
msg.reply_to = subscription
msg.topic = 'CameraGateway.{}.SetConfig'.format(camera_id)
msg.pack(set_config)
channel.publish(msg)

while True:
    msg = channel.consume()
    if msg.status.code == StatusCode.OK:
        log.info('Configuration applied on camera \'{}\'.', camera_id)
    else:
        log.warn('Can\'t apply configuration:\n{}', msg.status)
    sys.exit(0)
