from typing import TypedDict, Optional

from Perplexity.utils import ReadOnly


class Data(ReadOnly):
    wss = 'wss://www.perplexity.ai/socket.io/?EIO=4&transport=websocket'
    userInfo = 'https://www.perplexity.ai/api/user'
    headers = {
        'user-agent': 'Ask/2.23.0/260161 (Android; Version 12; samsung SM-G988N/z3qksx-user 12 NRD90M 1201230922 release-keys) SDK 32'
    }
    ask = {
        'android_device_id': 'cc199ca91e009c93',
        'conversational_enabled': True,
        'is_related_query': False,
        'is_voice_to_voice': False,
        'language': 'ru-RU',
        'mode': 'concise',
        'timezone': 'Africa/Nairobi',
        'use_inhouse_model': False
    }
    source = {
        'source': 'android',
        'version': '2.4'
    }


class UserInfo(TypedDict):
    id: str
    username: str
    email: str
    subscription_status: str
    subscription_source: str
    created: bool
    is_in_organization: bool
    name: Optional[str]
