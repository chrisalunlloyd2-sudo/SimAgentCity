# TIMESTAMP: 2026-06-08T10:00:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-Tester

import asyncio
import websockets
import json

async def test_ws():
    uri = "ws://localhost:8000/ws/chat"
    try:
        print(f"[TESTER] Connecting to {uri}...")
        async with websockets.connect(uri) as websocket:
            print("[TESTER] Connected successfully.")
            # Send a dummy message
            await websocket.send("test")
            # Wait for any broadcast (if backend sends one immediately)
            msg = await asyncio.wait_for(websocket.recv(), timeout=5)
            print(f"[TESTER] Received: {msg}")
            print("[TESTER] WebSocket bus is OPERATIONAL.")
    except Exception as e:
        print(f"[TESTER] WebSocket FAILED: {e}")

asyncio.run(test_ws())
