import asyncio
from typing import List

from app.db import fetch_session_events, finalize_session
from app.llm import stream_llm_response


async def generate_session_summary(session_id: str):
    """
    Background task that:
    1. Fetches session conversation
    2. Uses Gemini to summarize it
    3. Saves summary back to the session record
    """

    events = fetch_session_events(session_id)

    if not events:
        finalize_session(session_id, summary="No conversation data.")
        return

    # Build conversation text
    conversation = ""
    for event in events:
        conversation += f"{event['role'].upper()}: {event['content']}\n"

    prompt = f"""
You are an AI assistant summarizing a conversation session.

Provide a concise, high-level summary (3–4 sentences max)
focusing on:
- main topics discussed
- user intent
- outcomes or conclusions

Conversation:
{conversation}
"""

    summary_text = ""

    async for chunk in stream_llm_response(prompt):
        summary_text += chunk

    finalize_session(session_id, summary=summary_text.strip())
