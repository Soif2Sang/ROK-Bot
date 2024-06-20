import asyncio
from asyncio import ProactorEventLoop, get_event_loop
import logging
from typing import List, Optional
import traceback

import fastapi
from fastapi import HTTPException, Request, WebSocket, WebSocketDisconnect, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from uvicorn import Config, Server
import json
import threading

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

# Define the FastAPI app creation function
def create_app(cors_origins: Optional[List[str]] = None):
    app = fastapi.FastAPI(
        title="Test App",
        debug=False,
    )

    @app.get("/health")
    async def health():
        return "The GLOW API server is healthy."

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return PlainTextResponse(str(exc), status_code=422)


    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                message = json.loads(data)
                action = message.get('action')

                if action == 'upload_config':
                    config.update(message.get('config', {}))
                    await manager.send_personal_message("Config uploaded", websocket)
                elif action == 'get_config':
                    await manager.send_personal_message(json.dumps(config), websocket)
                elif action == 'start':
                    task_id = message.get('task_id')
                    tasks[task_id] = threading.Thread(target=start_task, args=(task_id,))
                    tasks[task_id].start()
                    await manager.broadcast(f"Task {task_id} started")
                elif action == 'pause':
                    task_id = message.get('task_id')
                    pause_task(task_id)
                    await manager.broadcast(f"Task {task_id} paused")
                elif action == 'stop':
                    task_id = message.get('task_id')
                    stop_task(task_id)
                    await manager.broadcast(f"Task {task_id} stopped")
                elif action == 'log':
                    log_message = message.get('log')
                    await manager.broadcast(f"Log: {log_message}")
        except WebSocketDisconnect:
            manager.disconnect(websocket)

    def start_task(task_id):
        try:
            # Replace the following line with the actual task logic
            # For demonstration, we'll just raise an exception
            raise Exception(f"Error occurred in task {task_id}")
        except Exception as e:
            tb_str = ''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
            # Broadcasting the traceback to all connected clients
            asyncio.run(manager.broadcast(f"Traceback for task {task_id}:\n{tb_str}"))

    def pause_task(task_id):
        # Logic to pause the task
        pass

    def stop_task(task_id):
        # Logic to stop the task
        pass

    return app

# Define a custom server class using ProactorEventLoop for Windows compatibility
class ProactorServer(Server):
    def run(self, sockets=None):
        loop = ProactorEventLoop()
        asyncio.set_event_loop(loop)
        asyncio.run(self.serve(sockets=sockets))

# Create the FastAPI app
app = create_app()
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

# Configure and run the server
config = Config(app=app, host="127.0.0.1", port=45632, log_level="info")
server = ProactorServer(config=config)
server.run()
