# WebSocket JSON Message Demo

This project is a small Python WebSocket example that uses a shared message protocol layer between a server and client.

## Project structure

- `server.py` — starts the WebSocket server and handles incoming client messages.
- `client.py` — connects to the server and sends JSON-encoded messages.
- `protocol.py` — defines the `Message` model and helper constructors for chat, join, and leave events.
- `requirements.txt` — Python dependencies for the project.

## Protocol format

Messages are exchanged as JSON objects in the following format:

```json
{"type": "chat", "data": {"message": "Hello!"}}
```

The protocol layer provides:

```python
from protocol import Message, chat_message

msg = chat_message("Hello!")
print(msg.to_json())

raw = '{"type": "chat", "data": {"message": "Hello!"}}'
parsed = Message.from_json(raw)
print(parsed.type)
print(parsed.data)
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the server

```bash
python server.py
```

You can also override the host and port with environment variables:

```bash
WS_HOST=127.0.0.1 WS_PORT=8765 python server.py
```

## Run the client

```bash
python client.py
```

Or pass a port explicitly:

```bash
python client.py 8765
```

## Example behavior

The client sends a chat message as JSON, and the server decodes it, prints the message, and echoes a response back using the same protocol structure.

Example request:

```json
{"type": "chat", "data": {"message": "Hello Server! 8765"}}
```

Example response:

```json
{"type": "chat", "data": {"message": "Echo: Hello Server! 8765"}}
```

## Requirements

```text
websockets==17.1
```
