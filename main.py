from websockets import connect, WebSocketClientProtocol
from asyncio import run, sleep, get_running_loop
from json import dumps, loads
from re import search
from typing import Self, TypedDict

from data import Data, Headers, URI, HandshakeData


class Text(TypedDict):
    answer: str
    web_results: list
    chunks: list
    extra_web_results: list


class ChatMessage:
    def __init__(self, websocket: WebSocketClientProtocol, prompt: str, index: int, chat_data: dict) -> None:
        self.websocket = websocket
        self.prompt = prompt
        self.index = index
        self.chatData = chat_data

    async def pending(self) -> Text:
        await self.websocket.send(f'{self.index}{dumps(["perplexity_ask", self.prompt, Data | self.chatData])}')
        while True:
            message = await self.websocket.recv()
            if message.split('[')[0] == '42':
                yield loads(loads(search(r'\d+(.+)', str(message)).group(1))[1].get('text'))
            elif message == '2':
                await self.websocket.send('3')
            else:
                await self.websocket.recv()
                await self.websocket.send('3')
                data = loads(search(r'\d+(.+)', message).group(1))[0]
                Perplexity.chatData = {
                    'last_backend_uuid': data.get('backend_uuid'),
                    'read_write_token': data.get('read_write_token')
                }
                break

    def __aiter__(self):
        return self.pending()


class Perplexity:
    websocket = None
    index = 420
    chatData = {}

    def __call__(self, prompt: str) -> ChatMessage:
        self.index += 1
        return ChatMessage(self.websocket, prompt, self.index, self.chatData)

    async def __aenter__(self) -> Self:
        return await self._createChat()

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.websocket.close()

    async def _ping(self) -> None:
        while True:
            await self.websocket.send('3')
            await sleep(10)

    async def _identify(self) -> None:
        await self.websocket.recv()
        await self.websocket.send('40')
        await self.websocket.recv()
        await self.websocket.send(f'{self.index}{dumps(["list_feed", HandshakeData])}')
        await self.websocket.recv()

    async def _createChat(self) -> Self:
        self.websocket = await connect(
            uri=URI,
            extra_headers=Headers
        )
        await self._identify()
        get_running_loop().create_task(self._ping())
        return self


async def main():
    async with Perplexity() as chat:
        async for message in chat('сколько будет 2 + 2'):
            print(message)
        async for message in chat('что я тебя до этого спросил'):
            print(message)


if __name__ == '__main__':
    run(main())
