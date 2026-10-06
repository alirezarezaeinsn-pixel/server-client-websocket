import asyncio
import os
import sys

import websockets as ws

from protocol import Message, chat_message

HOST = os.getenv("WS_HOST", "127.0.0.1")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.getenv("WS_PORT", "54721"))


async def main():
    uri = f"ws://{HOST}:{PORT}"
    print(f"Connecting to WebSocket server at {uri}...")
    async with ws.connect(uri) as websocket:
        print(f"Connected to WebSocket server at {uri}!")
        message = chat_message(f"Hello Server! {PORT}")
        print(f"Sending: {message.to_json()}")
        await websocket.send(message.to_json())

        response = Message.from_json(await websocket.recv())
        print(f"Server response type: {response.type}")
        print(f"Server response data: {response.data}")


if __name__ == "__main__":
    asyncio.run(main())
