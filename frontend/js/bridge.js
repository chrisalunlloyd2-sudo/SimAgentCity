async function fetchMap() {
    try {
        const response = await fetch('/map');
        const data = await response.json();
        updateEngineEntities(data.files);
    } catch (e) {
        console.error("Pulse Link Failed", e);
    }
}

function updateEngineEntities(files) {
    if (!window.cityEngine) return;
    
    // Map files to random positions for now
    window.cityEngine.entities = files.map((f, i) => ({
        x: (i % 10) + 2,
        y: Math.floor(i / 10) + 2,
        type: 'file',
        name: f.name,
        id: f.path
    }));
}

// Step 5: 1.2s Pulse Handshake (JS Side)
setInterval(() => {
    fetchMap();
    const indicator = document.getElementById('pulse-indicator');
    indicator.style.opacity = indicator.style.opacity == '1' ? '0.3' : '1';
}, 1200);
