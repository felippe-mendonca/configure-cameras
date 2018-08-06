import sys
from is_wire.core import Channel, Subscription, Message, Logger
from is_wire.core.wire.status import StatusCode
from is_msgs.common_pb2 import FieldSelector
from is_msgs.camera_pb2 import CameraConfigFields, CameraConfig
from google.protobuf.json_format import Parse

uri = 'amqp://10.10.2.15:30000'
channel = Channel(uri)
subscription = Subscription(channel)
log = Logger(name='GetConfig')
camera_id = 0

get_config = FieldSelector()
get_config.fields.append(CameraConfigFields.Value('SAMPLING_SETTINGS'))
get_config.fields.append(CameraConfigFields.Value('IMAGE_SETTINGS'))

msg = Message()
msg.topic = 'CameraGateway.{}.GetConfig'.format(camera_id)
msg.reply_to = subscription
msg.pack(get_config)
channel.publish(msg)

while True:
    msg = channel.consume()
    if msg.status.code == StatusCode.OK:
        config = msg.unpack(CameraConfig)
        log.info('Configuration received from camera \'{}\'\n{}', camera_id, config)
    else:
        log.warn('Can\'t apply configuration:\n{}', msg.status)
    sys.exit(0)
