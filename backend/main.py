from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Sandbox handshake
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import AgentCityOrchestrator
from core.registry_bridge import RegistryBridge
from core.agent_registrar import AgentRegistrar
from core.telemetry_monitor import TelemetryMonitor

app = FastAPI(title="SimAgentCity API")

# Initialize Orchestrator on a default workspace
WORKSPACE = os.path.join(os.getcwd(), "city_workspace")
orchestrator = AgentCityOrchestrator(WORKSPACE)
registry = RegistryBridge()
registrar = AgentRegistrar(os.path.join(os.getcwd(), "agents_population.json"))
telemetry = TelemetryMonitor()

# Mount Frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

class TaskRequest(BaseModel):
    agent_id: str
    file_path: str
    task: str

class MoveRequest(BaseModel):
    source: str
    destination: str

class RegistryUpdateRequest(BaseModel):
    hive: str = "HKEY_CURRENT_USER"
    subkey: str
    value_name: str
    value: str

class AgentRegisterRequest(BaseModel):
    name: str
    role: str

@app.get("/map")
async def get_map():
    """Returns the city file topology."""
    return {"files": orchestrator.bridge.get_file_tree()}

@app.get("/registry")
async def get_registry_map(hive: str = "HKEY_CURRENT_USER", subkey: str = "Software"):
    """Returns registry keys as buildings."""
    return {"keys": registry.get_keys(hive, subkey)}

@app.post("/registry/update")
async def update_registry(req: RegistryUpdateRequest):
    """Allows agents to renovate registry buildings."""
    success, msg = registry.write_value(req.hive, req.subkey, req.value_name, req.value)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "SUCCESS", "message": msg}

@app.post("/move")
async def move_entity(req: MoveRequest):
    """Physically moves a file based on UI interaction."""
    success, msg = orchestrator.bridge.move_file(req.source, req.destination)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "SUCCESS", "message": msg}

@app.post("/mall/register")
async def register_agent(req: AgentRegisterRequest):
    """Adds a new agent sim to the population."""
    agent = registrar.register_agent(req.name, req.role)
    return {"status": "SUCCESS", "agent": agent}

@app.get("/mall/agents")
async def get_mall_agents():
    """Lists all agents available in the mall."""
    return {"agents": registrar.get_registered_agents()}

@app.post("/assign")
async def assign_task(req: TaskRequest):
    """Assigns an agent to a file task."""
    orchestrator.assign_task(req.agent_id, req.file_path, req.task)
    return {"status": "QUEUED", "agent": req.agent_id}

@app.get("/agents")
async def get_agents():
    """Returns status of all active sims."""
    return orchestrator.active_agents

@app.get("/vitals")
async def get_vitals():
    """Returns real-time city metabolism stats."""
    return telemetry.get_city_vitals()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
