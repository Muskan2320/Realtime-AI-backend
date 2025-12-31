import os
import uuid
from datetime import datetime, timezone

from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase environment variables not set")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create_session(session_id: str, user_id: str | None = None):
    supabase.table("sessions").insert({
        "session_id": session_id,
        "user_id": user_id,
        "start_time": datetime.utcnow().isoformat()
    }).execute()

def log_event(session_id: str, role: str, content: str, event_type: str):
    supabase.table("events").insert({
        "event_id": str(uuid.uuid4()),
        "session_id": session_id,
        "role": role,
        "content": content,
        "event_type": event_type,
    }).execute()
# event_type can be 'user_message', 'ai_chunk'

def finalize_session(session_id: str, summary: str):
    result = supabase.table("sessions").select("start_time").eq("session_id", session_id).single().execute()
    
    start_time = datetime.fromisoformat(result.data["start_time"])
    end_time = datetime.now(timezone.utc)
    
    duration_seconds = int((end_time - start_time).total_seconds())

    supabase.table("sessions").update({
        "end_time": end_time.isoformat(),
        "duration_seconds": duration_seconds,
        "summary": summary
    }).eq("session_id", session_id).execute()

def fetch_session_events(session_id: str):
    """
    Fetch all events for a session in chronological order.
    Used for post-session summarization.
    """
    result = (
        supabase
        .table("events")
        .select("role, content")
        .eq("session_id", session_id)
        .order("created_at")
        .execute()
    )

    return result.data or []
