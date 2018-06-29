from is_wire.core import Channel, Subscription, Message, Logger
from is_msgs.camera_pb2 import CameraConfig
from google.protobuf.json_format import Parse

# necessery to create a CameraConfig message
from google.protobuf.wrappers_pb2 import FloatValue
from is_msgs.common_pb2 import SamplingSettings
from is_msgs.image_pb2 import ImageSettings, Resolution, ColorSpace, ColorSpaces

uri = 'amqp://10.10.2.15:30000'
c = Channel(uri)
sb = Subscription(c)
log = Logger()
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

def on_set_config(msg, context):
    print(msg.metadata())

def set_config_timeouted(msg, context):
    log.warn('SetConfig request timeout exceeded')

msg = Message()
msg.pack(set_config)
msg.set_reply_to(sb)
msg.set_on_reply(on_set_config)
msg.set_timeout_ms(5000) # not needed
msg.set_on_timeout(set_config_timeouted)  # not needed
msg.set_topic('CameraGateway.{}.SetConfig'.format(camera_id))
c.publish(msg)

c.listen()