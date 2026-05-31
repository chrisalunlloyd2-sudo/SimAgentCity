// TIMESTAMP: 2026-05-26T11:56:15.123Z
// PROJECT_ID: SimAgentCity-v1.3
// AGENT_ID: Antigravity-Architect

async function fetchMap() {
    try {
        const response = await fetch('/map');
        const data = await response.json();
        updateEngineEntities(data.files, 'file');
    } catch (e) {
        console.error("Pulse Link Failed", e);
    }
}

async function fetchRegistry() {
    try {
        const response = await fetch('/registry');
        const data = await response.json();
        updateEngineEntities(data.keys, 'registry');
    } catch (e) {
        console.error("Registry Link Failed", e);
    }
}

async function recruitAgent() {
    const name = document.getElementById('reg-name').value;
    const role = document.getElementById('reg-role').value;
    const risk_profile = document.getElementById('reg-risk').value;
    if (!name) return alert("Enter Agent Name");
    
    try {
        const response = await fetch('/mall/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, role, risk_profile})
        });
        const data = await response.json();
        alert(`Agent ${data.agent.name} recruited to the city!`);
        fetchMallAgents();
    } catch (e) {
        console.error("Recruitment Failed", e);
    }
}

async function fetchMallAgents() {
    try {
        const response = await fetch('/mall/agents');
        const data = await response.json();
        
        // Also fetch active status for stamina/xp
        const activeRes = await fetch('/agents');
        const activeData = await activeRes.json();
        
        // Merge data for rendering
        const mergedAgents = data.agents.map(a => {
            const activeInfo = activeData[a.id] || {};
            return { ...a, active: activeInfo };
        });
        
        updateEngineEntities(mergedAgents, 'agent');
        
        // Update Agent List UI
        document.getElementById('agent-count').innerText = `Active Population: ${mergedAgents.length}`;
        const listView = document.getElementById('agent-list-view');
        listView.innerHTML = mergedAgents.map(a => `
            <div style="border-bottom: 1px dashed #c0c0c0; padding: 5px;">
                <strong>${a.name}</strong> [${a.role}]<br>
                Wallet: <span style="font-size: 10px;">${a.wallet.substring(0, 10)}...</span><br>
                Stamina: ${a.active.stamina !== undefined ? a.active.stamina : a.traits.stamina}% | Logic: Lvl ${a.traits.logic_level}
            </div>
        `).join('');
    } catch (e) {
        console.error("Mall Link Failed", e);
    }
}

async function fetchBankLedger() {
    try {
        const response = await fetch('/bank/ledger');
        const data = await response.json();
        
        document.getElementById('city-funds').innerText = `${data.total_funds.toLocaleString()} PYTHON_COIN`;
        const ledgerView = document.getElementById('bank-ledger-view');
        
        if (data.ledger && data.ledger.length > 0) {
            ledgerView.innerHTML = data.ledger.map(txn => `
                <div style="border-bottom: 1px dotted #ccc; padding: 2px; font-family: monospace;">
                    [${new Date(txn.timestamp * 1000).toLocaleTimeString()}] 
                    <strong>${txn.sender}</strong> -> <strong>${txn.receiver}</strong>: ${txn.amount} ${txn.currency}<br>
                    Hash: <span style="color:#808080">${txn.hash.substring(0, 16)}...</span>
                </div>
            `).reverse().join('');
        } else {
            ledgerView.innerHTML = "<em>No blocks mined yet.</em>";
        }
    } catch (e) {}
}

// Retro Web Audio Sound Synthesizer (Phase 5 premium UI feedback)
function playRetroSound(type) {
    try {
        const AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        const ctx = new AudioCtx();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);

        if (type === 'drop') {
            // Classic SimCity 1995 placement sine swoop
            osc.type = 'sine';
            osc.frequency.setValueAtTime(450, ctx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(150, ctx.currentTime + 0.15);
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.15);
            osc.start();
            osc.stop(ctx.currentTime + 0.15);
        } else if (type === 'recruit') {
            // Joyful retro chime
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
            osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.08); // E5
            osc.frequency.setValueAtTime(783.99, ctx.currentTime + 0.16); // G5
            osc.frequency.setValueAtTime(1046.50, ctx.currentTime + 0.24); // C6
            gain.gain.setValueAtTime(0.2, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.45);
            osc.start();
            osc.stop(ctx.currentTime + 0.45);
        } else if (type === 'bulldoze') {
            // Low rumble / explosion
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(120, ctx.currentTime);
            osc.frequency.linearRampToValueAtTime(30, ctx.currentTime + 0.25);
            gain.gain.setValueAtTime(0.3, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.25);
            osc.start();
            osc.stop(ctx.currentTime + 0.25);
        } else if (type === 'query') {
            // Short retro beep
            osc.type = 'sine';
            osc.frequency.setValueAtTime(800, ctx.currentTime);
            gain.gain.setValueAtTime(0.1, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.08);
            osc.start();
            osc.stop(ctx.currentTime + 0.08);
        }
    } catch (err) {
        console.warn("Audio Context blocked or not supported", err);
    }
}
window.playRetroSound = playRetroSound;

// Missing Bridge Functions: Zoning, Vitals, Security, Processes

async function fetchZones() {
    try {
        const response = await fetch('/zoning');
        const data = await response.json();
        if (window.cityEngine) {
            window.cityEngine.zones = data;
        }
    } catch (e) {
        console.error("Zoning Link Failed", e);
    }
}

async function updateZone(x, y, zoneType) {
    try {
        const response = await fetch('/zoning/update', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({x, y, zone_type: zoneType})
        });
        const data = await response.json();
        if (data.status === 'SUCCESS') {
            console.log(`[ZONE] Zone updated at ${x},${y} to ${zoneType}`);
            fetchZones();
        }
    } catch (e) {
        console.error("Zoning Update Failed", e);
    }
}
window.updateZone = updateZone;

async function fetchVitals() {
    try {
        const response = await fetch('/vitals');
        const data = await response.json();
        if (data.status === "OFFLINE") return;
        
        document.getElementById('vit-cpu').innerText = `${data.hardware_bus.cpu_load.toFixed(1)}%`;
        document.getElementById('vit-net').innerText = `${data.hardware_bus.net_traffic_kbps.toFixed(1)} kbps`;
        document.getElementById('vit-weather').innerText = data.city_weather;
        document.getElementById('vit-stress').innerText = data.city_stress;
    } catch (e) {
        console.error("Vitals Link Failed", e);
    }
}

async function fetchSecurityStatus() {
    try {
        const response = await fetch('/security/status');
        const data = await response.json();
        
        // Populate Trust Graph
        const trustGraphView = document.getElementById('trust-graph-view');
        if (trustGraphView) {
            const keys = Object.keys(data.trust_graph);
            if (keys.length > 0) {
                trustGraphView.innerHTML = keys.map(k => `
                    <div style="border-bottom: 1px dashed #ccc; padding: 2px;">
                        Agent: <strong>${k}</strong> | Multiplier: <span style="color:green; font-weight:bold;">${data.trust_graph[k]}x</span>
                    </div>
                `).join('');
            } else {
                trustGraphView.innerHTML = "<em>No trust proofs minted yet.</em>";
            }
        }
        
        // Populate Quarantine / Interpol
        const secPopulation = document.getElementById('sec-population');
        if (secPopulation) secPopulation.innerText = data.interpol.monitored_population;
        
        const secStatus = document.getElementById('sec-status');
        if (secStatus) secStatus.innerText = data.interpol.status;
        
        const quarantineListView = document.getElementById('quarantine-list-view');
        if (quarantineListView) {
            const quarantined = data.interpol.quarantined_agents;
            if (quarantined.length > 0) {
                quarantineListView.innerHTML = quarantined.map(q => `
                    <div style="font-weight: bold; padding: 2px;">
                        ⚠️ WARNING: Agent ${q} is QUARANTINED!
                    </div>
                `).join('');
            } else {
                quarantineListView.innerHTML = "<em style='color:green;'>No anomalous behaviors detected. System safe.</em>";
            }
        }
    } catch (e) {
        console.error("Security Link Failed", e);
    }
}

async function mintAgentTrust() {
    const agentId = document.getElementById('mint-agent-id').value;
    const workProof = document.getElementById('mint-work-proof').value;
    
    if (!agentId || !workProof) return alert("Please fill both Agent ID and Work Proof fields.");
    
    try {
        const response = await fetch('/security/mint', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                agent_id: agentId,
                physical_work_data: workProof
            })
        });
        const data = await response.json();
        alert(`ASIC Proof-of-Work Minted! Trust Multiplier: ${data.trust_multiplier}x`);
        playRetroSound('recruit');
        
        // Clear fields and refresh
        document.getElementById('mint-agent-id').value = '';
        document.getElementById('mint-work-proof').value = '';
        fetchSecurityStatus();
    } catch (e) {
        alert("Failed to mint trust.");
    }
}
window.mintAgentTrust = mintAgentTrust;

let selectedPid = null;

async function fetchProcesses() {
    try {
        const response = await fetch('/processes');
        const data = await response.json();
        
        updateEngineEntities(data.processes, 'process');
        
        // Populate Task Manager UI
        const processListView = document.getElementById('process-list-view');
        if (processListView) {
            processListView.innerHTML = data.processes.map(p => `
                <div class="process-item" style="border-bottom: 1px dotted #ccc; padding: 4px; cursor: pointer; display: flex; justify-content: space-between; font-size: 11px;" onclick="selectProcess(${p.pid}, this)">
                    <span><strong>${p.name}</strong> (PID: ${p.pid})</span>
                    <span>CPU: ${p.cpu.toFixed(1)}% | Mem: ${p.mem_mb} MB</span>
                </div>
            `).join('');
        }
    } catch (e) {
        console.error("Processes Link Failed", e);
    }
}

function selectProcess(pid, element) {
    selectedPid = pid;
    playRetroSound('query');
    
    // Highlight element
    document.querySelectorAll('.process-item').forEach(el => {
        el.style.backgroundColor = 'transparent';
        el.style.color = '#000';
    });
    element.style.backgroundColor = '#000080';
    element.style.color = '#fff';
}
window.selectProcess = selectProcess;

async function demolishSelectedProcess() {
    if (!selectedPid) return alert("Select a process from the list first.");
    if (confirm(`Are you sure you want to demolish Process PID: ${selectedPid}? This will terminate the process on your system!`)) {
        playRetroSound('bulldoze');
        try {
            const response = await fetch(`/demolish/process`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ pid: selectedPid })
            });
            const data = await response.json();
            alert(data.message || "Process demolished!");
            selectedPid = null;
            fetchProcesses();
        } catch (e) {
            alert("Failed to demolish process.");
        }
    }
}
window.demolishSelectedProcess = demolishSelectedProcess;

function updateEngineEntities(items, type) {
    if (!window.cityEngine) return;
    
    // Filter existing entities of other types
    const otherEntities = window.cityEngine.entities.filter(e => e.type !== type);
    
    const newEntities = items.map((item, i) => {
        let x, y, color;
        if (type === 'file') {
            x = (i % 8) + 2; y = Math.floor(i / 8) + 2; color = '#ff0';
        } else if (type === 'registry') {
            x = (i % 8) + 15; y = Math.floor(i / 8) + 2; color = '#0ff';
        } else if (type === 'agent') {
            x = (i % 5) + 2; y = Math.floor(i / 5) + 15; color = '#f00';
        } else if (type === 'process') {
            x = (i % 5) + 15; y = Math.floor(i / 5) + 15; color = '#7f7f7f';
        }

        return {
            x, y, type, color,
            name: item.name || item.id || String(item.pid),
            id: item.path || item.id || String(item.pid),
            data: item // Store full item for inspector
        };
    });

    window.cityEngine.entities = [...otherEntities, ...newEntities];
}

// Spatial drag and drop logic
async function syncMovement(entity, isoPos) {
    if (!window.cityEngine) return;
    
    // 1. Detect drop onto Agent
    const targetAgent = window.cityEngine.entities.find(
        ent => ent.x === isoPos.x && ent.y === isoPos.y && ent.type === 'agent' && ent !== entity
    );
    
    if (targetAgent) {
        const task = prompt(`Assign task to Agent ${targetAgent.name} for file ${entity.name}:`, "Process this file.");
        if (task) {
            playRetroSound('recruit');
            try {
                const response = await fetch('/assign', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        agent_id: targetAgent.id,
                        file_path: entity.id,
                        task: task
                    })
                });
                alert(`Task successfully queued for Agent ${targetAgent.name}!`);
            } catch (e) {
                console.error("Task Assignment Failed", e);
            }
        }
        return;
    }
    
    // 2. Detect drop onto Folder
    const targetFolder = window.cityEngine.entities.find(
        ent => ent.x === isoPos.x && ent.y === isoPos.y && ent.type === 'file' && ent.id.indexOf('.') === -1 && ent !== entity
    );
    
    if (targetFolder) {
        const sourcePath = entity.id;
        const destPath = targetFolder.id + '/' + entity.name;
        playRetroSound('drop');
        try {
            const response = await fetch('/move', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    source: sourcePath,
                    destination: destPath
                })
            });
            console.log(`[GOD_HAND] Moved file physically: ${sourcePath} -> ${destPath}`);
            fetchMap();
        } catch (e) {
            console.error("File Move Failed", e);
        }
        return;
    }
    
    // 3. Detect drop in Specialized Zoning
    const zone = window.cityEngine.zones[`${isoPos.x},${isoPos.y}`];
    if (zone && zone !== 'RESIDENTIAL') {
        const agents = window.cityEngine.entities.filter(ent => ent.type === 'agent');
        
        let matchedAgent = null;
        if (zone === 'MINING') {
            matchedAgent = agents.find(a => a.data.role === 'Miner');
        } else if (zone === 'PROCESSING') {
            matchedAgent = agents.find(a => a.data.role === 'Processor');
        } else if (zone === 'INDUSTRIAL') {
            matchedAgent = agents.find(a => a.data.role === 'Shipper');
        }
        
        if (!matchedAgent) {
            matchedAgent = agents[0]; // Fallback to any agent
        }
        
        if (matchedAgent) {
            const task = zone === 'MINING' ? "Scan and mine this file." : 
                         (zone === 'PROCESSING' ? "Summarize and process this file." : "Ship this file to GitHub.");
                         
            console.log(`[ZONE_AUTO_ASSIGN] Zoning matched! Routing ${entity.name} to Agent ${matchedAgent.name} (Role: ${matchedAgent.data.role})`);
            playRetroSound('recruit');
            try {
                await fetch('/assign', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        agent_id: matchedAgent.id,
                        file_path: entity.id,
                        task: task
                    })
                });
            } catch (e) {
                console.error("Zoning assignment failed", e);
            }
        }
    }
}

// Step 5: 1.2s Pulse Handshake (JS Side)
setInterval(() => {
    fetchMap();
    fetchRegistry();
    fetchMallAgents();
    fetchZones();
    fetchVitals();
    fetchBankLedger();
    fetchProcesses();
    fetchSecurityStatus();
    const indicator = document.getElementById('pulse-indicator');
    indicator.style.opacity = indicator.style.opacity == '1' ? '0.3' : '1';
}, 1200);

// Link interactions
window.onload = () => {
    // Initial fetches
    fetchMap();
    fetchRegistry();
    fetchMallAgents();
    fetchZones();
    fetchVitals();
    fetchBankLedger();
    fetchProcesses();
    fetchSecurityStatus();

    if (window.cityEngine && window.CityInput) {
        window.cityInput = new CityInput(window.cityEngine, { 
            syncMovement,
            onInspect: (entity) => {
                if (window.currentTool !== 'tool-query') return;
                const win = document.getElementById('win-inspector');
                const content = document.getElementById('inspector-content');
                win.style.display = 'flex';
                
                if (entity.type === 'agent') {
                    const activeStamina = entity.data.active.stamina !== undefined ? entity.data.active.stamina : entity.data.traits.stamina;
                    const activeStatus = entity.data.active.status || entity.data.status;
                    const activeThought = entity.data.active.thought || "Idle";
                    
                    content.innerHTML = `
                        <strong>Name:</strong> ${entity.name}<br>
                        <strong>Role:</strong> ${entity.data.role}<br>
                        <strong>Status:</strong> ${activeStatus}<br>
                        <strong>Thought:</strong> <em>"${activeThought}"</em><br>
                        <hr>
                        <strong>Wallet:</strong> <span style="font-size:10px">${entity.data.wallet}</span><br>
                        <strong>Stamina:</strong> ${activeStamina}%<br>
                        <strong>Logic Level:</strong> ${entity.data.traits.logic_level}<br>
                        <strong>Risk Profile:</strong> ${entity.data.traits.risk_profile}<br>
                    `;
                } else if (entity.type === 'process') {
                    content.innerHTML = `
                        <strong>Name:</strong> ${entity.name}<br>
                        <strong>Type:</strong> OS Process<br>
                        <strong>PID:</strong> ${entity.id}<br>
                        <strong>CPU Usage:</strong> ${entity.data.cpu.toFixed(1)}%<br>
                        <strong>Memory:</strong> ${entity.data.mem_mb} MB
                    `;
                } else {
                    content.innerHTML = `
                        <strong>Name:</strong> ${entity.name}<br>
                        <strong>Type:</strong> ${entity.type}<br>
                        <strong>Path:</strong> ${entity.id}
                    `;
                }
            }
        });
    }
};
