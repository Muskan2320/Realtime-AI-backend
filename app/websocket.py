from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import uuid
import asyncio

from app.db import create_session, log_event, finalize_session
from app.llm import stream_llm_response
from app.post_session import generate_session_summary

websocket_router = APIRouter()

@websocket_router.websocket("/ws/session")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    create_session(session_id=session_id)

    try:
        await websocket.send_text(f"Connected to session {session_id}")

        while True:
            user_message = await websocket.receive_text()
            log_event(session_id=session_id, role="user", content=user_message, event_type="user_message")

            full_response = ""
            async for token in stream_llm_response(user_message):
                full_response += token
                await websocket.send_text(token)

                log_event(session_id=session_id, role="assistant", content=token, event_type="ai_chunk")

            log_event(session_id=session_id, role="assistant", content=full_response, event_type="ai_final")

    except WebSocketDisconnect:
        asyncio.create_task(generate_session_summary(session_id=session_id))
        print(f"Session {session_id} disconnected")
        