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

// UI Toggles
document.getElementById('tool-mall').onclick = () => {
    const form = document.getElementById('recruitment-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
};

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
        }

        return {
            x, y, type, color,
            name: item.name || item.id,
            id: item.path || item.id,
            data: item // Store full item for inspector
        };
    });

    window.cityEngine.entities = [...otherEntities, ...newEntities];
}

// Step 5: 1.2s Pulse Handshake (JS Side)
setInterval(() => {
    fetchMap();
    fetchRegistry();
    fetchMallAgents();
    fetchZones();
    fetchVitals();
    fetchBankLedger();
    const indicator = document.getElementById('pulse-indicator');
    indicator.style.opacity = indicator.style.opacity == '1' ? '0.3' : '1';
}, 1200);

// Link interactions
window.onload = () => {
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
