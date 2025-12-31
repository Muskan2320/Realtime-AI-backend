# Realtime AI Backend (WebSockets + Supabase + Gemini)

This project implements a **high-performance, asynchronous real-time AI backend** using **FastAPI**, **WebSockets**, **Supabase (Postgres)**, and **Gemini LLM**.  
It demonstrates real-time bi-directional communication, token-level LLM streaming, persistent session logging, and post-session automation.

The focus of this project is **backend architecture and system design**, not UI.

---

## 🚀 Features

- Real-time WebSocket sessions
- Token-by-token LLM streaming
- Stateful conversation handling
- Persistent session & event logging (Supabase Postgres)
- Background post-session summarization using Gemini
- Clean separation of concerns (WebSocket, DB, LLM, background jobs)

---

## 🏗️ Architecture Overview

```
Client (Browser / Simple UI)
        │
        │  WebSocket (bi-directional)
        ▼
FastAPI Backend
 ├── WebSocket Session Manager
 ├── Gemini LLM Streaming
 ├── Session State Management
 ├── Supabase Persistence Layer
 └── Background Post-Session Processor
        │
        ▼
Supabase Postgres
 ├── sessions
 └── events
```

---

## 📁 Project Structure

```
realtime-ai-backend/
│
├── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── websocket.py         # WebSocket lifecycle & streaming
│   ├── db.py                # Supabase DB operations
│   ├── llm.py               # Gemini streaming integration
│   └── post_session.py      # Background summarization job
│
├── sql/
│   └── schema.sql           # Supabase database schema
│
├── requirements.txt
├── .env                     # Environment variables (not committed)
└── README.md
```

---

## 🗄️ Database Schema (Supabase)

This project uses **two tables**:

- `sessions` → high-level session metadata
- `events` → chronological event log (user messages, AI tokens, etc.)

### 📄 `sql/schema.sql`

```sql
create table if not exists public.sessions (
    session_id uuid primary key,
    user_id text,
    start_time timestamptz not null default now(),
    end_time timestamptz,
    duration_seconds integer,
    summary text,
    created_at timestamptz default now()
);

create table if not exists public.events (
    event_id uuid primary key,
    session_id uuid references public.sessions(session_id) on delete cascade,
    role text not null,
    content text,
    event_type text not null,
    created_at timestamptz not null default now()
);
```

---

## 🔧 How to Apply the Schema in Supabase

1. Go to **Supabase Dashboard**
2. Open your project
3. Click **SQL Editor**
4. Paste the contents of `sql/schema.sql`
5. Click **Run**

Done ✅

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
GEMINI_API_KEY=your_gemini_api_key
```

⚠️ Never commit `.env` to GitHub.

---

## 📦 Installation

```bash
pip install -r requirements.txt
```


## ▶️ Running the Server

```bash
uvicorn app.main:app --reload
```

Server will be available at:
```
http://127.0.0.1:8000
```

---

## 🔌 WebSocket Usage

The WebSocket endpoint can be interacted with in **two different ways**: directly from JavaScript (for quick testing) or via the provided UI.

---

### **Option 1: Direct WebSocket usage (Browser Console / Script)**

This approach is useful for **quick testing or debugging** without using a UI.

```js
const ws = new WebSocket("ws://localhost:8000/ws/session");

ws.onmessage = (e) => console.log(e.data);

ws.onopen = () => {
  ws.send("Explain WebSocket streaming");
};
```

In this mode:
- A WebSocket connection is opened manually  
- A new session is created on connect  
- Messages are sent programmatically  
- LLM responses are streamed back in real time via `onmessage`

---

### **Option 2: UI-based usage (`index.html`)**

A minimal HTML client (`index.html`) is included to demonstrate a clean,
user-friendly real-time interaction.

In this mode:
- The WebSocket connection is established automatically when the page loads  
- Session setup messages are displayed before the conversation starts  
- User messages are sent only after the connection is ready  
- LLM responses stream live into the UI  

This approach better represents a **real-world chat interface** and is recommended for demos and reviews.

---

The same backend supports **both interaction patterns** without any code changes, demonstrating flexibility and reusability.

---

## 🧠 Post-Session Processing

On WebSocket disconnect:

1. Background async task is triggered
2. Conversation history is reconstructed from events
3. Gemini generates a concise summary
4. Summary is persisted to the sessions table

---


This project is intentionally backend-focused and designed to demonstrate production-grade AI system architecture.
