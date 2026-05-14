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
from core.road_builder import RoadBuilder
from core.agent_container import AgentContainerManager
from core.zoning_manager import ZoningManager
from tools.task_mgr_mini import get_process_summary, kill_process

app = FastAPI(title="SimAgentCity API")

# Initialize Orchestrator on a default workspace
WORKSPACE = os.path.join(os.getcwd(), "city_workspace")
orchestrator = AgentCityOrchestrator(WORKSPACE)
registry = RegistryBridge()
registrar = AgentRegistrar(os.path.join(os.getcwd(), "agents_population.json"))
telemetry = TelemetryMonitor()
roads = RoadBuilder(WORKSPACE)
containers = AgentContainerManager(WORKSPACE)
zoning = ZoningManager(os.path.join(os.getcwd(), "city_zoning.json"))

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
    risk_profile: str = "Balanced"

class ZoneUpdateRequest(BaseModel):
    x: int
    y: int
    zone_type: str

@app.get("/map")
async def get_map():
    """Returns the city file topology."""
    return {"files": orchestrator.bridge.get_file_tree()}

@app.get("/bank/ledger")
async def get_bank_ledger():
    """Returns the immutable bank ledger for the Bank Monitor UI."""
    # Assuming orchestrator has bank_ledger
    return {"ledger": orchestrator.bank_ledger, "total_funds": 10000 - len(orchestrator.bank_ledger) * 10}

@app.get("/zoning")
async def get_all_zones():
    """Returns the functional zoning of the grid."""
    return zoning.get_all_zones()

@app.post("/zoning/update")
async def update_zone(req: ZoneUpdateRequest):
    """Updates the functional role of a grid tile."""
    zoning.set_zone(req.x, req.y, req.zone_type)
    return {"status": "SUCCESS"}

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
    """Adds a new agent sim to the population and spawns their physical home."""
    agent = registrar.register_agent(req.name, req.role, req.risk_profile)
    # Step 201-300: Physical Spawning
    success, msg = containers.spawn_agent_home(agent["id"])
    if not success:
        raise HTTPException(status_code=500, detail=f"Registration failed: {msg}")
    return {"status": "SUCCESS", "agent": agent, "environment": msg}

@app.get("/mall/agents/stats")
async def get_agent_storage_stats(agent_id: str):
    """Checks disk usage of an agent's sandbox."""
    return containers.get_agent_storage_stats(agent_id)

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

@app.get("/transit")
async def get_transit_mapping(mode: str = "TCP"):
    """Returns the city transit mapping (TCP=WALK, UDP=BIKE, FTP=ROAD)."""
    return roads.protocol_dispatch({}, mode)

@app.get("/processes")
async def get_processes():
    """Returns OS processes as system buildings."""
    return {"processes": get_process_summary()}

@app.post("/demolish/process")
async def demolish_process(pid: int):
    """Kills an OS process by demolishing its sprite."""
    success, msg = kill_process(pid)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "SUCCESS", "message": msg}

@app.post("/bulldoze")
async def bulldoze_entity(path: str):
    """Step 101-150: Safe deletion protocol."""
    success, msg = roads.bulldoze(path)
    if not success:
        raise HTTPException(status_code=400, detail=msg)
    return {"status": "SUCCESS", "message": msg}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
