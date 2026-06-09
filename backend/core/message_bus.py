# TIMESTAMP: 2026-06-08T08:00:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-SymphonyBus

import asyncio
from typing import List
from fastapi import WebSocket

class SymphonyBus:
    """Centralized, thread-safe asynchronous MessageBus."""
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, data: dict):
        """Asynchronously broadcast data to all active WebSocket clients."""
        # DIAGNOSTIC TRACE
        with open("trace_diagnostic.log", "a") as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] BUS BROADCAST: {json.dumps(data)}\n")

        if not self.connections: return
        # Create tasks for all dispatches to prevent blocking
        await asyncio.gather(
            *[conn.send_json(data) for conn in self.connections],
            return_exceptions=True
        )

# Global Instance
bus = SymphonyBus()
