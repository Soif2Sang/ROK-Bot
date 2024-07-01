import asyncio
import threading
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from tasks.Worker_runner import WorkerRunner
from utils.singletons import ss
from utils.context import contextManager

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ss.open_emulator_settings()
ss.open_worker_settings()
ss.open_application_settings()
# Store connected clients
clients = {}

@app.get("/")
async def get():
    return HTMLResponse("WebSocket server is running")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    clients[client_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # Process incoming messages
            command = data.split(":")[0]
            worker_id = data.split(":")[1]

            if command.lower() == 'start':
                await websocket.send_text(f'Start command received for worker {worker_id}!')
                if contextManager.tasks.get(worker_id) and contextManager.tasks.get(worker_id).status == "running":
                    await websocket.send_text(f'Task is already running for worker {worker_id}.')
                else:
                    contextManager.start(worker_id, WorkerRunner(worker_id, contextManager))

            elif command.lower() == 'stop':
                await websocket.send_text(f'Stop command received for worker {worker_id}!')
                if not contextManager.tasks.get(worker_id) or contextManager.tasks.get(worker_id).status != "running":
                    await websocket.send_text(f'No task is running for worker {worker_id}.')
                else:
                    contextManager.get_worker(worker_id).stop(None)

            elif command.lower() == 'pause':
                await websocket.send_text(f'Pause command received for worker {worker_id}!')
                if not contextManager.tasks.get(worker_id) or contextManager.tasks.get(worker_id).status != "running":
                    await websocket.send_text(f'No task is running for worker {worker_id}.')
                else:
                    contextManager.get_worker(worker_id).pause(None)

    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
        del clients[client_id]

@app.get("/get-emulators-configurations")
async def get_emulators_configurations():
    return JSONResponse(ss.application_settings.to_dict())

@app.get("/get-workers-configurations")
async def get_workers_configurations():
    return JSONResponse(ss.worker_settings.to_dict())

@app.get("/get-application-configurations")
async def get_application_configurations():
    return JSONResponse(ss.application_settings.to_dict())

def start_worker(worker_id):
    worker = contextManager.get_worker(worker_id)
    worker.start(None)
    send_update_to_client(worker_id, "Job is done")

def send_update_to_client(worker_id, message):
    for client_id, websocket in clients.items():
        try:
            asyncio.run(websocket.send_text(f'Worker {worker_id}: {message}'))
        except RuntimeError:
            pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
