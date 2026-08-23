import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Irish Aunt Leaderboard", layout="centered")

st.markdown(
    """
    <style>
    .stApp { background-color: #F5F5DC; }
    h1 { color: #165B33; font-family: sans-serif; text-align: center; }
    p { color: #333; text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("☘️ Irish Aunt Leaderboard & Behavior Log")
st.write(
    "Drag the ☰ handle to reorder (place close together for ties). Add notes"
    " about behavior below and save your snapshot!"
)

# Combined Drag-and-Drop, Irish Theme, and Behavior Notes Component
irish_app_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
        margin: 0; padding: 10px; background-color: #F5F5DC; color: #1a1a1a; 
    }
    .section-title { color: #165B33; border-bottom: 2px solid #D4AF37; padding-bottom: 5px; margin-top: 25px; font-size: 20px; }
    
    .list { list-style: none; padding: 0; margin: 0 0 20px 0; }
    .item { 
        display: flex; align-items: center; justify-content: space-between;
        background: #ffffff; margin-bottom: 10px; padding: 14px 18px; 
        border-radius: 8px; border: 2px solid #165B33;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        font-size: 18px; font-weight: bold; color: #165B33;
        touch-action: none;
    }
    .item.dragging { opacity: 0.5; background: #FFFDD0; border: 2px dashed #D4AF37; }
    
    .rank { 
        color: #D4AF37; background: #165B33; padding: 2px 8px; 
        border-radius: 4px; font-size: 16px; margin-right: 15px; width: 25px; text-align: center;
    }
    .name { flex-grow: 1; color: #222; }
    .handle { cursor: grab; font-size: 22px; color: #888; padding-left: 15px; }
    
    .notes-container {
        background: #ffffff; padding: 15px; border-radius: 8px;
        border: 2px solid #165B33; margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .notes-field {
        width: 100%; padding: 10px; margin-top: 5px; margin-bottom: 12px;
        border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box;
        font-family: inherit; font-size: 14px;
    }
    .notes-label { font-weight: bold; color: #165B33; font-size: 15px; }

    .btn {
        background: #165B33; color: #FFFDD0; border: 2px solid #D4AF37; padding: 14px 20px;
        font-size: 16px; border-radius: 8px; cursor: pointer; width: 100%;
        font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    .btn:active { background: #0b301a; }

    .history-box {
        background: #ffffff; padding: 14px; border-radius: 8px; margin-bottom: 12px;
        font-size: 14px; border-left: 5px solid #165B33; border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .history-time { font-weight: bold; color: #165B33; margin-bottom: 6px; }
    .history-notes { margin-top: 6px; color: #444; font-style: italic; white-space: pre-wrap; }
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

<div class="notes-container">
    <div class="notes-label">📝 Aunt Behavior Notes:</div>
    <textarea id="behaviorNotes" class="notes-field" rows="3" placeholder="Log any notable behavior, comments, or drama today..."></textarea>
</div>

<button class="btn" onclick="saveSnapshot()">📸 Save Snapshot & Notes</button>

<div class="section-title">📜 Saved Snapshot History</div>
<div id="historyContainer"></div>

<script>
    const board = document.getElementById('board');
    let dragged = null;

    window.onload = function() { 
        updateRanks(); 
        renderHistory();
    };

    // Touch and drag support for mobile
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
            } else {
                return closest;
            }
        }, { offset: Number.NEGATIVE_INFINITY }).element;
    }

    // Tie calculation based on vertical closeness
    function updateRanks() {
        const items = [...board.querySelectorAll('.item')];
        let currentRank = 1;

        items.forEach((item, index) => {
            const rankSpan = item.querySelector('.rank');
            if (index > 0) {
                const prevItem = items[index - 1];
                const prevBox = prevItem.getBoundingClientRect();
                const currBox = item.getBoundingClientRect();
                
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

        const notes = document.getElementById('behaviorNotes').value;

        const now = new Date();
        const timeString = now.toLocaleDateString() + ' at ' + now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});

        let history = JSON.parse(localStorage.getItem('irish_aunt_device_history') || '[]');
        history.unshift({ time: timeString, order: currentOrder, notes: notes });
        
        localStorage.setItem('irish_aunt_device_history', JSON.stringify(history));
        
        // Clear notes field and refresh view
        document.getElementById('behaviorNotes').value = '';
        renderHistory();
        alert('Snapshot & Notes saved successfully!');
    }

    function renderHistory() {
        const container = document.getElementById('historyContainer');
        let history = JSON.parse(localStorage.getItem('irish_aunt_device_history') || '[]');
        
        if (history.length === 0) {
            container.innerHTML = '<p style="color: #666; font-style: italic;">No snapshots saved yet.</p>';
            return;
        }

        let html = '';
        history.forEach(entry => {
            let notesHtml = entry.notes ? `<div class="history-notes">📝 Notes: ${entry.notes}</div>` : '';
            html += `<div class="history-box">
                <div class="history-time">🕒 ${entry.time}</div>
                <div><b>Ranks:</b> ${entry.order.join(' | ')}</div>
                ${notesHtml}
            </div>`;
        });
        container.innerHTML = html;
    }
</script>
</body>
</html>
"""

# Render the application cleanly on Streamlit
components.html(irish_app_code, height=850)
