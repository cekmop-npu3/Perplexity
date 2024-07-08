from re import search
from websockets import connect, WebSocketClientProtocol
from websockets.exceptions import ConnectionClosedOK
from json import dumps, loads
from typing import Self, Optional, Literal, AsyncIterator
from aiohttp import ClientSession
from uuid import uuid4

from Perplexity.data import Data, UserInfo


__all__ = (
    'Perplexity',
)


class Connector:
    def __init__(self, token: str, chatId: str = None) -> None:
        self.token = token
        self.chatId = chatId
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.chatData = {}

    async def connect(self) -> None:
        self.websocket = await connect(
            uri=Data.wss,
            extra_headers=Data.headers
        )
        await self.websocket.recv()
        await self.websocket.send(f'40{dumps({"perplexity_jwt": self.token})}')
        if (await self.websocket.recv()).startswith('44'):
            raise ValueError('Invalid auth token')
        await self.websocket.recv()
        if self.chatId:
            await self.websocket.send(
                f'420{dumps(["get_thread_by_uuid", self.chatId, Data.source | {"with_parent_info": True}])}'
            )
            if isinstance(data := loads(search(r'\d+(.+)', await self.websocket.recv()).group(1))[0], dict):
                raise ValueError('Invalid chatId or auth token')
            self.chatData = self.chatData if self.chatData else {'last_backend_uuid': data[-1].get('backend_uuid'), 'read_write_token': data[-1].get('read_write_token')}

    async def deleteChat(self) -> None:
        if self.websocket is None:
            raise NotImplementedError('Websocket has not been connected')
        if not self.chatId:
            raise NotImplementedError('ChatId has not been set or provided')
        await self.websocket.send(f'420{dumps(["delete_thread_by_entry_uuid", self.chatId, {"read_write_token": self.chatData.get("read_write_token"), "source": "android", "version": "2.4"}])}')
        await self.websocket.recv()

    async def getUserInfo(self) -> UserInfo:
        async with ClientSession() as session:
            async with session.get(
                url=Data.userInfo,
                headers=Data.headers | {'authorization': f'Bearer {self.token}'}
            ) as response:
                return await response.json()


class Messages:
    def __init__(self, connector: Connector, prompt: str, searchFocus: Literal['internet', 'scholar', 'writing', 'wolfram', 'youtube', 'reddit'] = 'internet') -> None:
        self.connector = connector
        self.prompt = prompt
        self.searchFocus = searchFocus

    async def ask(self) -> None:
        try:
            await self.connector.websocket.send(f'420{dumps(["perplexity_ask", self.prompt, Data.ask | {"frontend_uuid": str(uuid4()), "search_focus": self.searchFocus, "user_nextauth_id": (await self.connector.getUserInfo()).get("id")} | Data.source | self.connector.chatData])}')
        except ConnectionClosedOK:
            await self.connector.connect()
            await self.ask()

    async def pending(self):
        await self.ask()
        while True:
            message = await self.connector.websocket.recv()
            if message.split('[')[0] == '42':
                yield loads(loads(search(r'\d+(.+)', str(message)).group(1))[1].get('text'))
            elif message == '2':
                await self.connector.websocket.send('3')
            else:
                data = loads(search(r'\d+(.+)', message).group(1))[0]
                self.connector.chatData = {'last_backend_uuid': (chatId := data.get('backend_uuid')), 'read_write_token': data.get('read_write_token')}
                self.connector.chatId = chatId
                break

    def __aiter__(self) -> AsyncIterator[str]:
        return self.pending()


class Perplexity:
    def __init__(self, *, token: str, chatId: str = None, searchFocus: Literal['internet', 'scholar', 'writing', 'wolfram', 'youtube', 'reddit'] = 'internet', deleteChat: bool = False) -> None:
        self.connector = Connector(token, chatId)
        self.searchFocus = searchFocus
        self.deleteChat = deleteChat

    def __call__(self, prompt: str) -> Messages:
        if not self.connector.websocket:
            raise SyntaxError(f'{self.__class__.__name__} class should be used via context manager')
        return Messages(self.connector, prompt, self.searchFocus)

    async def __aenter__(self) -> Self:
        await self.connector.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.deleteChat:
            await self.connector.deleteChat()
        await self.connector.websocket.close()

    def __init_subclass__(cls, **kwargs) -> None:
        raise SyntaxError(f'{cls.__base__.__name__} class cannot be inherited')
