# Replace the layout_html section with this
st.subheader("Design Your Layout")
layout_html = f"""
<div id="layout-container" style="width: 500px; height: 300px; border: 1px solid #ccc; position: relative;">
    {''.join([f'<div class="draggable" style="position: absolute; width: 100px; height: 50px; background: #e0e0e0; cursor: move; top: {i*60}px;" data-id="{i}">{section_names[i]}</div>' for i in range(num_sections)])}
</div>
<script>
    const container = document.getElementById('layout-container');
    const draggables = document.getElementsByClassName('draggable');
    let layoutData = [];

    function updateLayout() {
        layoutData = [];
        for (let i = 0; i < draggables.length; i++) {
            const rect = draggables[i].getBoundingClientRect();
            layoutData.push({
                id: draggables[i].getAttribute('data-id'),
                x: rect.left - container.getBoundingClientRect().left,
                y: rect.top - container.getBoundingClientRect().top
            });
        }
        window.parent.postMessage({type: 'layout_update', data: layoutData}, '*');
    }

    for (let i = 0; i < draggables.length; i++) {
        draggables[i].addEventListener('mousedown', startDragging);
    }

    function startDragging(e) {
        const draggable = e.target;
        let shiftX = e.clientX - draggable.getBoundingClientRect().left;
        let shiftY = e.clientY - draggable.getBoundingClientRect().top;

        function moveAt(pageX, pageY) {
            draggable.style.left = pageX - shiftX - container.getBoundingClientRect().left + 'px';
            draggable.style.top = pageY - shiftY - container.getBoundingClientRect().top + 'px';
        }

        function onMouseMove(e) {
            moveAt(e.pageX, e.pageY);
        }

        document.addEventListener('mousemove', onMouseMove);

        document.onmouseup = function() {
            document.removeEventListener('mousemove', onMouseMove);
            document.onmouseup = null;
            updateLayout();
        };
    }

    document.addEventListener('dragstart', (e) => e.preventDefault());
</script>
"""
layout_component = components.html(layout_html, height=320, scrolling=True)
if st.button("Save Layout"):
    # This would ideally capture the layout_data from the component, but requires additional JS-Python bridging
    st.session_state["layout_data"] = [{"id": i, "x": 0, "y": i*60} for i in range(num_sections)]  # Placeholder
layout_data = st.session_state.get("layout_data", [])
