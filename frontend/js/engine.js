const canvas = document.getElementById('city-canvas');
const ctx = canvas.getContext('2d');

canvas.width = canvas.parentElement.clientWidth;
canvas.height = canvas.parentElement.clientHeight;

const tileSize = 32;
const gridColor = '#006400';

class CityEngine {
    constructor() {
        this.entities = []; // {x, y, type, id, name}
        this.camera = {x: 0, y: 0};
        this.init();
    }

    init() {
        window.addEventListener('resize', () => {
            canvas.width = canvas.parentElement.clientWidth;
            canvas.height = canvas.parentElement.clientHeight;
            this.draw();
        });
        this.animate();
    }

    drawGrid() {
        ctx.strokeStyle = gridColor;
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += tileSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, canvas.height);
            ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += tileSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvas.width, y);
            ctx.stroke();
        }
    }

    drawEntities() {
        this.entities.forEach(ent => {
            ctx.fillStyle = ent.color || '#fff';
            ctx.fillRect(ent.x * tileSize, ent.y * tileSize, tileSize - 2, tileSize - 2);
            
            // Retro labels
            ctx.fillStyle = '#fff';
            ctx.font = '10px "MS Sans Serif"';
            const displayName = ent.name.length > 10 ? ent.name.substring(0, 8) + '..' : ent.name;
            ctx.fillText(displayName, ent.x * tileSize, ent.y * tileSize - 5);
        });
    }

    drawDistricts() {
        ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
        ctx.font = '20px "MS Sans Serif"';
        ctx.fillText("FILE MALL", 2 * tileSize, 2 * tileSize - 10);
        ctx.fillText("REGISTRY PLAZA", 15 * tileSize, 2 * tileSize - 10);
        ctx.fillText("AGENT DISTRICT", 2 * tileSize, 15 * tileSize - 10);
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
