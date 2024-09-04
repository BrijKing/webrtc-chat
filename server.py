import asyncio
import websockets
import json

connected_clients = set()

async def signaling_server(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            for client in connected_clients:
                if client != websocket:
                    await client.send(json.dumps(data))
    finally:
        connected_clients.remove(websocket)

start_server = websockets.serve(signaling_server, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

