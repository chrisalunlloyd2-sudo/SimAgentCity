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
    if (!name) return alert("Enter Agent Name");
    
    try {
        const response = await fetch('/mall/register', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({name, role})
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
        document.getElementById('agent-count').innerText = `Agents: ${data.agents.length}`;
    } catch (e) {
        console.error("Mall Link Failed", e);
    }
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
            id: item.path || item.id
        };
    });

    window.cityEngine.entities = [...otherEntities, ...newEntities];
}

// UI Toggles
document.getElementById('tool-mall').onclick = () => {
    const form = document.getElementById('recruitment-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
};

// Initialized by engine.js
async function fetchMap() {
...
}

// Step 451-500: UI Feedback Loop
async function syncMovement(entity, newIsoPos) {
    if (entity.type === 'file') {
        const dest = `moved_${Math.random().toString(36).substring(7)}_${entity.name}`;
        try {
            const response = await fetch('/move', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    source: entity.id,
                    destination: dest
                })
            });
            const data = await response.json();
            if (data.status === 'SUCCESS') {
                console.log("[BRIDGE] Physical Move Verified");
            }
        } catch (e) {
            console.error("[BRIDGE] Move Failed", e);
        }
    }
}

// Step 5: 1.2s Pulse Handshake (JS Side)
setInterval(() => {
...
}, 1200);

// Link interactions
window.onload = () => {
    if (window.cityEngine && window.CityInput) {
        window.cityInput = new CityInput(window.cityEngine, { syncMovement });
    }
};
