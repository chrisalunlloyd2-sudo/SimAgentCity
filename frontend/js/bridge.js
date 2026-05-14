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
        updateEngineEntities(data.agents, 'agent');
        
        // Update Agent List UI
        document.getElementById('agent-count').innerText = `Active Population: ${data.agents.length}`;
        const listView = document.getElementById('agent-list-view');
        listView.innerHTML = data.agents.map(a => `
            <div style="border-bottom: 1px dashed #c0c0c0; padding: 5px;">
                <strong>${a.name}</strong> [${a.role}]<br>
                Risk: ${a.traits.risk_profile} | Trust: ${a.traits.trust_score} | Budget: §${a.traits.budget_limit}
            </div>
        `).join('');
    } catch (e) {
        console.error("Mall Link Failed", e);
    }
}

async function fetchVitals() {
    try {
        const response = await fetch('/vitals');
        const data = await response.json();
        if (data.status === 'OFFLINE') return;
        
        document.getElementById('vit-cpu').innerText = `${data.hardware_bus.city_pollution}%`;
        document.getElementById('vit-net').innerText = `${data.hardware_bus.city_wind_speed} knots`;
        document.getElementById('vit-weather').innerText = data.city_weather;
        document.getElementById('vit-stress').innerText = data.city_stress;
    } catch (e) {}
}

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

async function fetchBankLedger() {
    try {
        const response = await fetch('/bank/ledger');
        const data = await response.json();
        
        document.getElementById('city-funds').innerText = `§ ${data.total_funds.toLocaleString()}`;
        const ledgerView = document.getElementById('bank-ledger-view');
        
        if (data.ledger && data.ledger.length > 0) {
            ledgerView.innerHTML = data.ledger.map(txn => `
                <div style="border-bottom: 1px dotted #ccc; padding: 2px;">
                    [${new Date(txn.timestamp * 1000).toLocaleTimeString()}] 
                    <strong>${txn.agent}</strong> paid §${txn.cost_coins} for <em>${txn.task}</em> -> <span style="color:green">${txn.status}</span>
                </div>
            `).reverse().join('');
        } else {
            ledgerView.innerHTML = "<em>No transactions cleared.</em>";
        }
    } catch (e) {}
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
                    content.innerHTML = `
                        <strong>Name:</strong> ${entity.name}<br>
                        <strong>ID:</strong> ${entity.id}<br>
                        <strong>Role:</strong> ${entity.data.role}<br>
                        <strong>Status:</strong> ${entity.data.status}<br>
                        <hr>
                        <strong>Risk Profile:</strong> ${entity.data.traits.risk_profile}<br>
                        <strong>Trust Score:</strong> ${entity.data.traits.trust_score}<br>
                        <strong>Budget Limit:</strong> §${entity.data.traits.budget_limit}<br>
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
