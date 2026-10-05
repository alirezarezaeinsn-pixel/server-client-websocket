import asyncio
import os
import socket
import sys
import websockets as ws

Host = '127.0.0.1'
Port = 54721


def get_available_port(host: str, port: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
            return port
        except OSError:
            sock.bind((host, 0))
            return sock.getsockname()[1]


async def handle_client(websocket, path=None):
    print(f"Client connected: {websocket.remote_address} | path={path}")

    try:
        async for message in websocket:
            print(f"Received message from {websocket.remote_address}: {message}")
            await websocket.send(message)
    except ws.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")


async def main():
    port = get_available_port(Host, Port)
    print(f"Starting WebSocket server at ws://{Host}:{port}...")    
    async with ws.serve(handle_client, Host, port) as server:
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
