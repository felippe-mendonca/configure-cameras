from is_wire.core import Channel, Subscription, Message, Logger
from is_msgs.common_pb2 import FieldSelector
from is_msgs.camera_pb2 import CameraConfigFields, CameraConfig
from google.protobuf.json_format import Parse

uri = 'amqp://10.10.2.15:30000'
c = Channel(uri)
sb = Subscription(c)
log = Logger()
camera_id = 0

def on_get_config(msg, context):
    config = msg.unpack(CameraConfig)
    print(config)

def get_config_timeouted(msg, context):
    log.warn('GetConfig request timeout exceeded')


get_config = FieldSelector()
get_config.fields.append(CameraConfigFields.Value('SAMPLING_SETTINGS'))
get_config.fields.append(CameraConfigFields.Value('IMAGE_SETTINGS'))

msg = Message()
msg.pack(get_config)
msg.set_reply_to(sb)
msg.set_on_reply(on_get_config)
msg.set_timeout_ms(5000)
msg.set_on_timeout(get_config_timeouted)
msg.set_topic('CameraGateway.{}.GetConfig'.format(camera_id))
c.publish(msg)

c.listen()