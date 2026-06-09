// TIMESTAMP: 2026-06-08T10:30:00Z
// PROJECT_ID: SimsMerged-v1.4.2
// AGENT_ID: Gemini-CLI-Architect-Fixer

// Audio Synth Engine (Phased Implementation)
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

function playChatNote(textPayload) {
    let hash = 0;
    for (let i = 0; i < textPayload.length; i++) hash = textPayload.charCodeAt(i) + ((hash << 5) - hash);
    const freq = 220 + (Math.abs(hash) % 440);
    
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    
    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
    gain.gain.setValueAtTime(0.05, audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
    
    osc.start();
    osc.stop(audioCtx.currentTime + 0.5);
}

// Robust WebSocket Chat Connection
function connectChatSocket() {
    console.log("[BRIDGE] Initializing WebSocket chat bus...");
    const chatSocket = new WebSocket('ws://localhost:8000/ws/chat');
    
    chatSocket.onopen = () => {
        console.log("[BRIDGE] Chat Socket Connected Successfully.");
        document.getElementById('telemetry-status').innerText = "ONLINE";
        document.getElementById('telemetry-status').style.color = "#0f0";
        
        // Final Diagnostic: Inject connection confirmation to chat log
        const log = document.getElementById('chat-view');
        if (log) {
            log.innerHTML += '<div class="msn-entry" style="color: #008000; font-weight: bold;">[SYSTEM] MSN_CHAT_BUS_ACTIVE: Ready.</div>';
            log.scrollTop = log.scrollHeight;
        }
    };
    
    chatSocket.onmessage = (event) => {
        const log = JSON.parse(event.data);
        const chatView = document.getElementById('chat-view');
        if (chatView) {
            chatView.innerHTML += `
                <div class="msn-entry">
                    <span class="msn-name">${log.agent}:</span> ${log.message}
                </div>
            `;
            chatView.scrollTop = chatView.scrollHeight;
            playChatNote(log.message);
        }
    };
    
    chatSocket.onclose = () => {
        console.warn("[BRIDGE] Chat Socket Disconnected. Reconnecting...");
        setTimeout(connectChatSocket, 2000);
    };
}
connectChatSocket();

// User Message Sender
async function sendUserMsnMessage() {
    const input = document.getElementById('msn-input');
    const message = input.value;
    if (!message) return;

    try {
        await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({agent: "User", message: message})
        });
        input.value = '';
    } catch (e) {
        console.error("Chat Send Failed", e);
    }
}
window.sendUserMsnMessage = sendUserMsnMessage;

// Legacy support: Poll as fallback if WebSocket fails
setInterval(() => {
    fetchMap();
    fetchRegistry();
    fetchMallAgents();
    fetchZones();
    fetchVitals();
    fetchBankLedger();
    fetchProcesses();
    fetchSecurityStatus();
    // Chat polling fallback
    fetch('/chat')
        .then(r => {
            return r.json();
        })
        .then(data => {
            const chatView = document.getElementById('chat-view');
            if (chatView && data.logs) {
                // Simplified rendering to avoid duplication issues
                chatView.innerHTML = data.logs.map(log => `
                    <div class="msn-entry">
                        <span class="msn-name">${log.agent}:</span> ${log.message}
                    </div>
                `).join('');
                chatView.scrollTop = chatView.scrollHeight;
            }
        })
        .catch(e => console.error("[DIAGNOSTIC] Chat poll error:", e));
}, 2000);
