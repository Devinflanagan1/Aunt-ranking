import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Irish Aunt Leaderboard", layout="centered")

# Irish-themed header styling in Streamlit
st.markdown(
    """
    <style>
    .main { background-color: #F5F5DC; }
    h1 { color: #165B33; font-family: sans-serif; text-align: center; }
    p { text-align: center; color: #333; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("☘️ Irish Aunt Leaderboard")
st.write(
    "Drag the ☰ handle to reorder. Drop items closely next to each other to"
    " create ties!"
)

# Embedded HTML/JS component with Irish styling and auto-tie calculations
irish_leaderboard_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
        margin: 0; padding: 10px; background-color: #F5F5DC; color: #1a1a1a; 
    }
    .list { list-style: none; padding: 0; margin: 0 0 20px 0; }
    .item { 
        display: flex; align-items: center; justify-content: space-between;
        background: #ffffff; margin-bottom: 10px; padding: 14px 18px; 
        border-radius: 8px; border: 2px solid #165B33;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        font-size: 18px; font-weight: bold; color: #165B33;
        touch-action: none;
        transition: background 0.2s;
    }
    .item.dragging { opacity: 0.5; background: #FFFDD0; border: 2px dashed #D4AF37; }
    
    .rank { 
        color: #D4AF37; background: #165B33; padding: 2px 8px; 
        border-radius: 4px; font-size: 16px; margin-right: 15px; width: 25px; text-align: center;
    }
    .name { flex-grow: 1; color: #222; }
    .handle { cursor: grab; font-size: 22px; color: #888; padding-left: 15px; }
    
    .btn {
        background: #165B33; color: #FFFDD0; border: 2px solid #D4AF37; padding: 12px 20px;
        font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%;
        font-weight: bold; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .btn:active { background: #0b301a; }
    
    h3 { color: #165B33; border-bottom: 2px solid #D4AF37; padding-bottom: 5px; margin-top: 30px; }
    .history-box {
        background: #ffffff; padding: 12px; border-radius: 8px; margin-bottom: 10px;
        font-size: 14px; border-left: 5px solid #165B33; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .history-time { font-weight: bold; color: #165B33; margin-bottom: 4px; }
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

<button class="btn" onclick="saveSnapshot()">📸 Save Snapshot to History</button>

<h3>📜 Past Changes</h3>
<div id="historyContainer"></div>

<script>
    const board = document.getElementById('board');
    let dragged = null;

    window.onload = function() {
        updateRanks();
        renderHistory();
    };

    // Touch Support for Mobile
    board.addEventListener('touchstart', e => {
        if(e.target.classList.contains('handle') || e.target.closest('.handle')) {
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
        updateRanks();
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

    // Smart tie detection: checks if items overlap or are tightly grouped vertically
    function updateRanks() {
        const items = [...board.querySelectorAll('.item')];
        let currentRank = 1;

        items.forEach((item, index) => {
            const rankSpan = item.querySelector('.rank');
            if (index > 0) {
                const prevItem = items[index - 1];
                const prevBox = prevItem.getBoundingClientRect();
                const currBox = item.getBoundingClientRect();
                
                // If current item center is very close to previous item center, count as a tie
                const distance = Math.abs((currBox.top + currBox.height/2) - (prevBox.top + prevBox.height/2));
                if (distance < (currBox.height * 0.7)) {
                    rankSpan.innerText = prevItem.querySelector('.rank').innerText;
                    return;
                }
            }
            rankSpan.innerText = currentRank;
            currentRank++;
        });
    }

    function saveSnapshot() {
        const items = board.querySelectorAll('.item');
        let currentOrder = [];
        items.forEach((item) => {
            let rank = item.querySelector('.rank').innerText;
            let name = item.querySelector('.name').innerText;
            currentOrder.push("#" + rank + " " + name);
        });

        const now = new Date();
        const timeString = now.toLocaleDateString() + ' at ' + now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        let history = JSON.parse(localStorage.getItem('irish_aunt_history') || '[]');
        history.unshift({ time: timeString, order: currentOrder });
        
        localStorage.setItem('irish_aunt_history', JSON.stringify(history));
        renderHistory();
    }

    function renderHistory() {
        const container = document.getElementById('historyContainer');
        let history = JSON.parse(localStorage.getItem('irish_aunt_history') || '[]');
        
        if (history.length === 0) {
            container.innerHTML = '<p style="color: #666; font-style: italic;">No snapshots saved yet.</p>';
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

components.html(irish_leaderboard_code, height=750)
