/**
 * Step 401-450: The God Hand Input Handler
 * Manages isometric drag-and-drop and entity selection.
 */

class CityInput {
    constructor(engine, bridge) {
        this.engine = engine;
        this.bridge = bridge;
        this.draggedEntity = null;
        this.offset = { x: 0, y: 0 };
        this.init();
    }

    // Step 401: Screen-to-Iso Coordinate Transformation
    screenToIso(screenX, screenY) {
        const relX = screenX - this.engine.camera.x;
        const relY = screenY - this.engine.camera.y;

        // Inverse Isometric Matrix
        // x = (relX / (tileW/2) + relY / (tileH/2)) / 2
        // y = (relY / (tileH/2) - relX / (tileW/2)) / 2
        const mapX = Math.floor((relX / (tileW / 2) + relY / (tileH / 2)) / 2);
        const mapY = Math.floor((relY / (tileH / 2) - relX / (tileW / 2)) / 2);

        return { x: mapX, y: mapY };
    }

    init() {
        const canvas = document.getElementById('city-canvas');

        canvas.addEventListener('mousedown', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            const isoPos = this.screenToIso(mouseX, mouseY);

            // Find entity at tile
            this.draggedEntity = this.engine.entities.find(ent => ent.x === isoPos.x && ent.y === isoPos.y);
            
            if (this.draggedEntity) {
                console.log(`[GOD_HAND] Grabbing ${this.draggedEntity.name}`);
                canvas.style.cursor = 'grabbing';
            }
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!this.draggedEntity) return;

            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            const isoPos = this.screenToIso(mouseX, mouseY);

            // Update entity position visually (Pre-sync)
            this.draggedEntity.x = isoPos.x;
            this.draggedEntity.y = isoPos.y;
        });

        window.addEventListener('mouseup', (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;
            const isoPos = this.screenToIso(mouseX, mouseY);

            // Handle Tools
            if (window.currentTool) {
                // If a tool is active, don't drop-move, apply tool action
                if (this.draggedEntity) {
                    this.draggedEntity.x = isoPos.x;
                    this.draggedEntity.y = isoPos.y;
                    this.draggedEntity = null;
                }

                const tool = window.currentTool;
                
                // Query Tool
                if (tool === 'tool-query') {
                    const target = this.engine.entities.find(ent => ent.x === isoPos.x && ent.y === isoPos.y);
                    if (target && this.bridge.onInspect) {
                        this.bridge.onInspect(target);
                    }
                } 
                // Bulldozer
                else if (tool === 'tool-bulldoze') {
                    const target = this.engine.entities.find(ent => ent.x === isoPos.x && ent.y === isoPos.y);
                    if (target) {
                        if (confirm(`Bulldoze ${target.name}?`)) {
                            // Backend API call to bulldoze
                            fetch('/bulldoze', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({path: target.id})
                            });
                        }
                    }
                }
                // Zoning Tools
                else if (tool.startsWith('tool-zone-')) {
                    let zoneType = "RESIDENTIAL";
                    if (tool === 'tool-zone-mine') zoneType = "MINING";
                    if (tool === 'tool-zone-proc') zoneType = "PROCESSING";
                    if (tool === 'tool-zone-ind') zoneType = "INDUSTRIAL";
                    
                    // Use bridge to update zone
                    if (window.updateZone) {
                        window.updateZone(isoPos.x, isoPos.y, zoneType);
                    }
                }

                canvas.style.cursor = 'default';
                window.currentTool = null;
                document.querySelectorAll('.tool-btn.icon-btn').forEach(b => b.classList.remove('active-tool'));
                return;
            }

            if (!this.draggedEntity) return;

            console.log(`[GOD_HAND] Dropping ${this.draggedEntity.name} at ${isoPos.x}, ${isoPos.y}`);
            
            // Trigger Backend Sync (Phase 2 Action Protocol)
            if (this.bridge.syncMovement) {
                this.bridge.syncMovement(this.draggedEntity, isoPos);
            }

            this.draggedEntity = null;
            canvas.style.cursor = 'default';
        });
    }
}

// Initialized by bridge.js
window.CityInput = CityInput;
