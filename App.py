import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Aunt Leaderboard", layout="centered")

st.title("🏆 Aunt Leaderboard")
st.write("Drag and drop to rank your aunts. Use **Save Snapshot** to log changes over time!")

drag_and_drop_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; margin: 0; padding: 10px; background: white; color: #333; }
    .list { list-style: none; padding: 0; margin: 0 0 20px 0; }
    .item { 
        display: flex; align-items: center; justify-content: space-between;
        background: #f8f9fa; margin-bottom: 10px; padding: 15px; 
        border-radius: 8px; border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 18px; font-weight: bold;
        touch-action: none;
    }
    .item.dragging { opacity: 0.5; background: #e2e8f0; border: 2px dashed #4793AF; }
    .rank { color: #888; font-size: 16px; margin-right: 15px; width: 25px; }
    .name { flex-grow: 1; }
    .handle { cursor: grab; font-size: 24px; color: #aaa; padding-left: 15px; }
    
    .btn {
        background: #007bff; color: white; border: none; padding: 12px 20px;
        font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%;
        font-weight: bold; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .btn:active { background: #0056b3; }
    
    h3 { border-bottom: 2px solid #eee; padding-bottom: 5px; margin-top: 30px; }
    .history-box {
        background: #f1f3f5; padding: 12px; border-radius: 8px; margin-bottom: 10px;
        font-size: 14px; border-left: 4px solid #007bff;
    }
    .history-time { font-weight: bold; color: #555; margin-bottom: 4px; }
</style>
</head>
<body>

<ul class="list" id="board">
    <li class="item" draggable="true"><span class="rank">1</span><span class="name">Nora</span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">2</span><span class="name">Anne</span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">3</span><span class="name">Janet</span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">4</span><span class="name">Cinta</span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">5</span><span class="name">Margo</span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">6</span><span class="name">Maureen</span><span class="handle">☰</span></li>
</ul>

<button class="btn" onclick="saveSnapshot()">📸 Save Current Ranking Snapshot</button>

<h3>📜 Ranking History</h3>
<div id="historyContainer"></div>

<script>
    const board = document.getElementById('board');
    let dragged = null;

    // Load saved history on startup
    window.onload = function() {
        renderHistory();
    };

    board.addEventListener('touchstart', e => {
        if(e.target.className === 'handle') {
            dragged = e.target.closest('.item');
            dragged.classList.add('dragging');
        }
    }, {passive: true});

    board.addEventListener('touchend', e => {
        if(dragged) {
            dragged.classList.remove('dragging');
            updateRanks();
            dragged = null;
        }
    });

    board.addEventListener('touchmove', e => {
        if(!dragged) return;
        e.preventDefault();
        const touch = e.touches[0];
        const afterElement = getDragAfterElement(board, touch.clientY);
        if (afterElement == null) {
            board.appendChild(dragged);
        } else {
            board.insertBefore(dragged, afterElement);
        }
    }, {passive: false});

    function getDragAfterElement(container, y) {
        const draggableElements = [...container.querySelectorAll('.item:not(.dragging)')];
        return draggableElements.reduce((closest, child) => {
            const box = child.getBoundingClientRect();
            const offset = y - box.top - box.height / 2;
            if (offset < 0 && offset > closest.offset) {
                return { offset: offset, element: child };
            } else { return closest; }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    function updateRanks() {
        const items = board.querySelectorAll('.item');
        items.forEach((item, index) => {
            item.querySelector('.rank').innerText = index + 1;
        });
    }

    function saveSnapshot() {
        const items = board.querySelectorAll('.item');
        let currentOrder = [];
        items.forEach((item, index) => {
            let name = item.querySelector('.name').innerText;
            currentOrder.push((index + 1) + ". " + name);
        });

        const now = new Date();
        const timeString = now.toLocaleDateString() + ' at ' + now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        let history = JSON.parse(localStorage.getItem('aunt_history') || '[]');
        history.unshift({ time: timeString, order: currentOrder }); // Add new to top
        
        localStorage.setItem('aunt_history', JSON.stringify(history));
        renderHistory();
    }

    function renderHistory() {
        const container = document.getElementById('historyContainer');
        let history = JSON.parse(localStorage.getItem('aunt_history') || '[]');
        
        if (history.length === 0) {
            container.innerHTML = '<p style="color: #778; font-style: italic;">No snapshots saved yet.</p>';
            return;
        }

        let html = '';
        history.forEach(entry => {
            html += `<div class="history-box">
                <div class="history-time">🕒 ${entry.time}</div>
                <div>${entry.order.join(' | ')}</div>
            </div>`;
        });
        container.innerHTML = html;
    }
</script>
</body>
</html>
"""

# Render in Streamlit with enough height to display history logs
components.html(drag_and_drop_code, height=750)
