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
            ctx.fillStyle = ent.type === 'agent' ? '#f00' : '#ff0';
            ctx.fillRect(ent.x * tileSize, ent.y * tileSize, tileSize - 2, tileSize - 2);
            
            // Retro labels
            ctx.fillStyle = '#fff';
            ctx.font = '10px "MS Sans Serif"';
            ctx.fillText(ent.name, ent.x * tileSize, ent.y * tileSize - 5);
        });
    }

    draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        this.drawGrid();
        this.drawEntities();
    }

    animate() {
        this.draw();
        requestAnimationFrame(() => this.animate());
    }
}

const engine = new CityEngine();
window.cityEngine = engine;
