import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Aunt Leaderboard", layout="centered")

st.title("🏆 Aunt Leaderboard")
st.write(
    "Press and hold the **☰** icon on your phone to drag and drop the"
    " rankings!"
)

# Embedded HTML/JS for separate tiles with a visual "TIED" badge
drag_and_drop_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; margin: 0; padding: 10px; background: white; }
    .list { list-style: none; padding: 0; margin: 0; }
    .item { 
        display: flex; align-items: center; justify-content: space-between;
        background: #f8f9fa; margin-bottom: 10px; padding: 15px; 
        border-radius: 8px; border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        font-size: 18px; font-weight: bold; color: #333;
        touch-action: none;
    }
    .item.dragging { opacity: 0.5; background: #e2e8f0; border: 2px dashed #4793AF; }
    .rank { color: #888; font-size: 16px; margin-right: 15px; width: 25px; }
    .name { flex-grow: 1; display: flex; align-items: center; gap: 10px; }
    .badge { 
        background: #ffc107; color: #333; font-size: 11px; 
        padding: 2px 6px; border-radius: 4px; font-weight: bold; 
        letter-spacing: 0.5px;
    }
    .handle { cursor: grab; font-size: 24px; color: #aaa; padding-left: 15px; }
</style>
</head>
<body>

<ul class="list" id="board">
    <li class="item" draggable="true"><span class="rank">1</span><span class="name">Nora</span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">2</span><span class="name">Anne</span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">3</span><span class="name">Janet <span class="badge">TIED</span></span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">4</span><span class="name">Cinta <span class="badge">TIED</span></span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">5</span><span class="name">Margo</span><span class="handle">☰</span></li>
    <li class="item" draggable="true"><span class="rank">6</span><span class="name">Maureen</span><span class="handle">☰</span></li>
</ul>

<script>
    const board = document.getElementById('board');
    let dragged = null;

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
</script>
</body>
</html>
"""

# Render the updated leaderboard in Streamlit (height increased to fit 6 tiles)
components.html(drag_and_drop_code, height=520)
