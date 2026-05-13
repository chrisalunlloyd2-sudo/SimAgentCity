const canvas = document.getElementById('city-canvas');
const ctx = canvas.getContext('2d');

canvas.width = canvas.parentElement.clientWidth;
canvas.height = canvas.parentElement.clientHeight;

const tileW = 64; // Isometric tile width
const tileH = 32; // Isometric tile height (2:1 ratio)
const gridColor = 'rgba(0, 100, 0, 0.5)';

class CityEngine {
    constructor() {
        this.entities = []; // {x, y, type, id, name, color}
        this.camera = { x: canvas.width / 2, y: 50 };
        this.init();
    }

    init() {
        window.addEventListener('resize', () => {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
            this.camera.x = canvas.width / 2;
            this.draw();
        });
        this.animate();
    }

    // Step 301-350: Isometric Transformation Matrix
    isoToScreen(mapX, mapY) {
        return {
            x: this.camera.x + (mapX - mapY) * (tileW / 2),
            y: this.camera.y + (mapX + mapY) * (tileH / 2)
        };
    }

    drawGrid() {
        ctx.strokeStyle = gridColor;
        ctx.lineWidth = 1;
        const gridSize = 20;

        for (let x = 0; x <= gridSize; x++) {
            let start = this.isoToScreen(x, 0);
            let end = this.isoToScreen(x, gridSize);
            ctx.beginPath();
            ctx.moveTo(start.x, start.y);
            ctx.lineTo(end.x, end.y);
            ctx.stroke();
        }
        for (let y = 0; y <= gridSize; y++) {
            let start = this.isoToScreen(0, y);
            let end = this.isoToScreen(gridSize, y);
            ctx.beginPath();
            ctx.moveTo(start.x, start.y);
            ctx.lineTo(end.x, end.y);
            ctx.stroke();
        }
    }

    drawDistricts() {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.font = 'bold 24px "MS Sans Serif"';
        
        const mall = this.isoToScreen(2, 2);
        ctx.fillText("FILE MALL", mall.x, mall.y);
        
        const plaza = this.isoToScreen(15, 2);
        ctx.fillText("REGISTRY PLAZA", plaza.x, plaza.y);
        
        const dist = this.isoToScreen(2, 15);
        ctx.fillText("AGENT DISTRICT", dist.x, dist.y);
    }

    drawEntities() {
        // Sort entities by depth (Y + X) for correct isometric layering
        const sorted = [...this.entities].sort((a, b) => (a.x + a.y) - (b.x + b.y));

        sorted.forEach(ent => {
            const pos = this.isoToScreen(ent.x, ent.y);
            
            // Draw Isometric Diamond/Cube Placeholder
            ctx.fillStyle = ent.color || '#fff';
            
            ctx.beginPath();
            ctx.moveTo(pos.x, pos.y - tileH/2); // Top
            ctx.lineTo(pos.x + tileW/2, pos.y); // Right
            ctx.lineTo(pos.x, pos.y + tileH/2); // Bottom
            ctx.lineTo(pos.x - tileW/2, pos.y); // Left
            ctx.closePath();
            ctx.fill();
            
            // Subtle 3D side shading
            ctx.fillStyle = 'rgba(0,0,0,0.2)';
            ctx.beginPath();
            ctx.moveTo(pos.x - tileW/2, pos.y);
            ctx.lineTo(pos.x, pos.y + tileH/2);
            ctx.lineTo(pos.x, pos.y + tileH);
            ctx.lineTo(pos.x - tileW/2, pos.y + tileH/2);
            ctx.fill();

            // Retro labels
            ctx.fillStyle = '#fff';
            ctx.font = '10px "MS Sans Serif"';
            const displayName = ent.name.length > 12 ? ent.name.substring(0, 10) + '..' : ent.name;
            ctx.fillText(displayName, pos.x - 20, pos.y - 20);
        });
    }

    draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        this.drawGrid();
        this.drawDistricts();
        this.drawEntities();
    }

    animate() {
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

const engine = new CityEngine();
window.cityEngine = engine;
