"""
Hack.chat Humbird

Minimal and fast chat bot template in Python.
Humble. Made to replace `foolishbird` as a bot template. Minimal like hummerbird.
One file. No importing[^1]. Less than 50 lines without comments.
Code by me(4n0n4me). WTFPL.
[^1]: You don't need to import humbird, as it is not a module or a library, but a complete bot.
"""


import json
import websocket


class Bot():
    def __init__(self, url: str, channel: str, nick: str, password: str = None):
        self.url = url
        self.nick = nick
        self.password = password
        self.channel = channel

    def run(self):
        self.ws = websocket.WebSocketApp(self.url)
        self.ws.on_open = self.on_open
        self.ws.on_message = self.on_message
        self.ws.run_forever(ping_interval=30)

    def send_chat(self, text: str) -> None:
        self.send({'cmd': 'chat', 'text': text})

    def send_whisper(self, text: str, nick: str) -> None:
        self.send({'cmd': 'whisper', 'nick': nick, 'text': text})

    def send(self, raw: dict) -> None:
        self.ws.send(json.dumps(raw))

    def on_open(self, ws):
        self.send({'cmd': 'join', 'channel': self.channel, 'nick': self.nick,
                   **({'password': self.password} if self.password else {})})

    def on_message(self, ws, message):
        msg: dict = json.loads(message)
        if msg.get('cmd') == 'chat' and msg.get('text') == 'ping':
            self.send_chat('pong')
        elif msg.get('cmd') == 'onlineSet':
            self.send_chat('Hello World!')


if __name__ == '__main__':
    bot = Bot('wss://hack.chat/chat-ws', 'your-channel', 'humbird')
    # With threading: (import threading at first)
    #
    # thread = threading.Thread(target=bot.run)
    # thread.start()
    # thread.join()
    #
    # Without threading:
    bot.run()
