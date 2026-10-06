import asyncio
import os
import socket
import websockets as ws

from protocol import Message, chat_message

Host = os.getenv("WS_HOST", "127.0.0.1")
Port = int(os.getenv("WS_PORT", "54721"))


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
        async for raw_message in websocket:
            try:
                message = Message.from_json(raw_message)
            except ValueError as exc:
                print(f"Received invalid JSON from {websocket.remote_address}: {exc}")
                await websocket.send(chat_message(f"Error: {exc}").to_json())
                continue

            print(
                f"Received message from {websocket.remote_address}: "
                f"type={message.type} data={message.data}"
            )

            if message.type == "chat":
                reply = chat_message(f"Echo: {message.data.get('message', '')}")
            else:
                reply = chat_message(f"Received {message.type}")

            await websocket.send(reply.to_json())
    except ws.exceptions.ConnectionClosed:
        print(f"Client disconnected: {websocket.remote_address}")


async def main():
    port = get_available_port(Host, Port)
    print(f"Starting WebSocket server at ws://{Host}:{port}...")
    async with ws.serve(handle_client, Host, port):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
