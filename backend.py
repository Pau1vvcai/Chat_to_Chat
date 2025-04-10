from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from urllib.parse import parse_qs

app = FastAPI()
connections = {}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    query = parse_qs(ws.url.query)
    username = query.get("username", ["Unknown"])[0]
    connections[ws] = username

    try:
        while True:
            msg = await ws.receive_text()
            sender = connections[ws]
            for conn, name in list(connections.items()):
                try:
                    await conn.send_text(f"{sender}::{msg}")
                except:
                    connections.pop(conn, None)
    except WebSocketDisconnect:
        connections.pop(ws, None)
