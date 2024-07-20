import asyncio
import json

import websockets
from realtime.connection import Socket

from constants import SUPABASE_ID, SUPABASE_KEY, SUPABASE_URL
from supabase_auth import SupabaseClient

CHANNEL = "room-1"
WSS_URL = f"wss://{SUPABASE_ID}.supabase.co/realtimeLocal/v1/websocket?apikey={SUPABASE_KEY}&vsn=1.0.0"

supabaseClient = SupabaseClient()
response = supabaseClient.login("maxou@gmail.com","maxou@gmail.com")

async def send_heartbeat(websocket, interval=30):
    while True:
        await asyncio.sleep(interval)
        await websocket.send(json.dumps({
            "event": "heartbeat",
            "topic": "phoenix",
            "payload": {},
            "ref": "heartbeat"
        }))
        print("Heartbeat sent")


async def connect_to_supabase():
    async with websockets.connect(WSS_URL) as websocket:
        # Authenticate
        await websocket.send(json.dumps({
            "event": "access_token",
            "topic": "realtimeLocal:*",
            "payload": {"access_token":  response.session.access_token},
            "ref": "1"
        }))

        # Subscribe to the channel with broadcast config
        await websocket.send(json.dumps({
            "event": "phx_join",
            "topic": f"realtme:{CHANNEL}",
            "payload": {
                "config": {
                    "broadcast": {"self": False, "private": True}
                }
            },
            "ref": "2"
        }))

        print(f"Subscribed to channel: {CHANNEL}")

        # Start sending heartbeat messages
        asyncio.create_task(send_heartbeat(websocket))

        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            handle_message(data)


def handle_message(data):
    event = data.get("event")

    if event == "broadcast":
        payload = data.get("payload")
        print(f"Received broadcast message: {payload}")
    elif event == "phx_reply":
        status = data.get("payload", {}).get("status")
        print(f"Reply status: {status}")
    elif event == "system":
        status = data.get("payload", {}).get("status")
        message = data.get("payload", {}).get("message")
        print(f"System message - Status: {status}, Message: {message}")
    else:
        print(f"Received unhandled message: {data}")


# Run the event loop
asyncio.get_event_loop().run_until_complete(connect_to_supabase())