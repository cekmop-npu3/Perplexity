from utils import DictMeta, Format
from uuid import uuid4


URI = 'wss://www.perplexity.ai/socket.io/?EIO=4&transport=websocket'


class Data(metaclass=DictMeta):
    source = 'android'
    version = '2.3'
    frontend_uuid = str(uuid4())
    use_inhouse_model = False
    conversational_enabled = True
    android_device_id = 'cc199ca91e009c93'
    mode = 'concise'
    search_focus = 'internet'
    is_related_query = False
    timezone = 'Africa/Nairobi'
    language = 'ru-RU'


class HandshakeData(metaclass=DictMeta):
    source = 'android'
    version = '2.3'
    offset = 0
    limit = 20


class Headers(metaclass=DictMeta):
    User_Agent = Format('Ask/2.18.2/260140 (Android; Version 12; samsung SM-G988N/z3qksx-user 12 NRD90M 1201230922 release-keys) SDK 32')
    X_App_Version = Format('2.18.2')
    X_Client_Version = Format('2.18.2')
    X_Client_Name = Format('Perplexity-Android')
    X_App_ApiClient = Format('android')
    X_App_ApiVersion = Format('2.3')
    Accept_Encoding = Format('gzip')
