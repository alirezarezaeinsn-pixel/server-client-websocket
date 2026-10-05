import asyncio
import os
import sys

import websockets as ws

HOST = '127.0.0.1'
PORT = 54721


async def main():
    uri = f"ws://{HOST}:{PORT}"
    print(f"Connecting to WebSocket server at {uri}...")
    async with ws.connect(uri) as websocket:
        print(f"Connected to WebSocket server at {uri}!")
        await websocket.send("Hello Server!")
        response = await websocket.recv()
        print(f"Server response: {response}")


if __name__ == "__main__":
    asyncio.run(main())
