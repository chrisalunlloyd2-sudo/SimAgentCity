// Win95 GUI Interactivity

function toggleWindow(id) {
    const el = document.getElementById(id);
    if (el.style.display === 'none') {
        el.style.display = 'flex';
        // Bring to front
        document.querySelectorAll('.win95-window').forEach(w => w.style.zIndex = 100);
        el.style.zIndex = 101;
    } else {
        el.style.display = 'none';
    }
}

// Draggable Windows
document.querySelectorAll('.win95-window').forEach(win => {
    const titlebar = win.querySelector('.win95-titlebar');
    let isDragging = false;
    let offsetX, offsetY;

    titlebar.addEventListener('mousedown', (e) => {
        if (e.target.classList.contains('win95-close')) return;
        isDragging = true;
        offsetX = e.clientX - win.getBoundingClientRect().left;
        offsetY = e.clientY - win.getBoundingClientRect().top;
        
        // Bring to front
        document.querySelectorAll('.win95-window').forEach(w => w.style.zIndex = 100);
        win.style.zIndex = 101;
    });

    window.addEventListener('mousemove', (e) => {
        if (isDragging) {
            win.style.left = (e.clientX - offsetX) + 'px';
            win.style.top = (e.clientY - offsetY) + 'px';
        }
    });

    window.addEventListener('mouseup', () => {
        isDragging = false;
    });
});

// SimCity Toolbar Logic
window.currentTool = null;

document.querySelectorAll('.tool-btn.icon-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        // Deselect all
        document.querySelectorAll('.tool-btn.icon-btn').forEach(b => b.classList.remove('active-tool'));
        
        if (window.currentTool === btn.id) {
            window.currentTool = null; // Toggle off
            document.getElementById('city-canvas').style.cursor = 'default';
        } else {
            window.currentTool = btn.id;
            btn.classList.add('active-tool');
            
            // Set cursor
            if (btn.id === 'tool-query') {
                document.getElementById('city-canvas').style.cursor = 'help';
            } else if (btn.id === 'tool-bulldoze') {
                document.getElementById('city-canvas').style.cursor = 'crosshair';
            } else {
                document.getElementById('city-canvas').style.cursor = 'crosshair';
            }
        }
    });
});
