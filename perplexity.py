from websockets import connect, WebSocketClientProtocol
from asyncio import run, sleep
from json import dumps, loads
from re import search
from uuid import uuid4

from typing import Self


class ChatMessage:
    def __init__(self, websocket: WebSocketClientProtocol, prompt: str, index: int, chat_data: dict) -> None:
        self.websocket = websocket
        self.prompt = prompt
        self.index = index
        self.chatData = chat_data

    async def pending(self):
        await self.websocket.send(
            f'{self.index}{dumps(["perplexity_ask", self.prompt, {"source": "android", "version": "2.3", "frontend_uuid": str(uuid4()), "use_inhouse_model": False, "conversational_enabled": True, "android_device_id": "cc199ca91e009c93", "mode": "concise", "search_focus": "internet", "is_related_query": False, "timezone": "Africa/Nairobi", "language": "ru-RU"} | self.chatData])}'
        )
        while (message := await self.websocket.recv()).split('[')[0] == '42':
            yield loads(search(r'\d+(.+)', message).group(1))
            await sleep(1)
        await self.websocket.recv()
        await self.websocket.send('3')
        data = loads(search(r'\d+(.+)', message).group(1))[0]
        Perplexity.chatData = {'last_backend_uuid': data.get('backend_uuid'), 'read_write_token': data.get('read_write_token')}
        yield data

    def __aiter__(self):
        return self.pending()


class Perplexity:
    websocket = None
    index = 40
    chatData = {}

    def __call__(self, prompt: str) -> ChatMessage:
        self.index += 1
        return ChatMessage(self.websocket, prompt, self.index, self.chatData)

    async def __aenter__(self) -> Self:
        return await self.createChat()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.websocket.close()

    async def identify(self, websocket: WebSocketClientProtocol):
        await websocket.recv()
        await websocket.send(str(self.index))
        await websocket.recv()
        self.index = 420
        await websocket.send(
            f'{self.index}{dumps(["list_feed",{"source": "android","version": "2.3","offset": 0,"limit": 20}])}'
        )
        await websocket.recv()

    async def createChat(self) -> Self:
        self.websocket = await connect(
            uri='wss://www.perplexity.ai/socket.io/?EIO=4&transport=websocket',
            extra_headers={
                "User-Agent": "Ask/2.18.2/260140 (Android; Version 12; samsung SM-G988N/z3qksx-user 12 NRD90M 1201230922 release-keys) SDK 32",
                "X-App-Version": "2.18.2",
                "X-Client-Version": "2.18.2",
                "X-Client-Name": "Perplexity-Android",
                "X-App-ApiClient": "android",
                "X-App-ApiVersion": "2.3",
                "Accept-Encoding": "gzip"
            }
        )
        await self.identify(self.websocket)
        return self


async def main():
    async with Perplexity() as chat:
        async for message in chat('what is 2 + 2'):
            print(message)
        async for message in chat('what have i asked you before'):
            print(message)
        async for message in chat('what have i asked you before'):
            print(message)


if __name__ == '__main__':
    run(main())
