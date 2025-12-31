from fastapi import FastAPI
from app.websocket import websocket_router

app = FastAPI(title = "Realtime AI Backend")

app.include_router(websocket_router)