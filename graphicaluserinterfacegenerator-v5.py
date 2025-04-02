# graphicaluserinterfacegeneratorv1.py
import streamlit as st
import requests
import json
import streamlit.components.v1 as components

# Title of the application
st.title("Graphical User Interface Generator")

# API Key input
api_key = st.text_input("Enter your Google AI Studio API Key", type="password")

# Programming languages dropdown
programming_languages = ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "PHP", "TypeScript", "Swift", "Kotlin", "Go", "Rust", "Scala", "Perl", "R"]
selected_language = st.selectbox("Select Programming Language", programming_languages)

# Frameworks dictionary categorized by type
frameworks = {
    "Python": {
        "Web Development": ["Django", "Flask", "FastAPI", "Tornado", "Bottle", "CherryPy", "Pyramid", "Sanic", "Falcon", "Hug", "Masonite", "Dash", "Streamlit"],
        "GUI": ["Tkinter", "PyQt", "PySide", "Kivy", "wxPython", "PyGTK", "Dear PyGui", "Toga", "Eel"],
        "Machine Learning/Data Science": ["TensorFlow", "PyTorch", "Scikit-learn", "Keras", "XGBoost", "LightGBM", "CatBoost", "Pandas", "NumPy", "SciPy"],
        "Testing": ["Pytest", "Unittest", "Nose2", "Robot Framework", "Behave", "Hypothesis"],
        "Networking/Asynchronous": ["Twisted", "AIOHTTP", "Gevent", "Eventlet"],
        "Game Development": ["Pygame", "Arcade", "Pyglet", "Panda3D"],
        "Other": ["SQLAlchemy", "Flask-RESTful", "Celery", "Scrapy", "Click", "Typer", "Jinja2", "Matplotlib", "Seaborn"]
    },
    "JavaScript": ["React", "Vue.js", "Angular", "Node.js", "Express"],
    "Java": ["Spring", "JavaFX", "Swing", "JSF", "Vaadin"],
    "C++": ["Qt", "wxWidgets", "FLTK", "GTK+"],
    "C#": [".NET", "WPF", "Windows Forms", "Xamarin"]
}

# Framework info with descriptions and documentation links
framework_info = {
    "Django": {"desc": "High-level web framework for rapid development.", "doc": "https://docs.djangoproject.com/"},
    "Flask": {"desc": "Lightweight microframework for web apps.", "doc": "https://flask.palletsprojects.com/"},
    "FastAPI": {"desc": "High-performance API framework with async support.", "doc": "https://fastapi.tiangolo.com/"},
    "Tornado": {"desc": "Asynchronous web framework for handling connections.", "doc": "https://www.tornadoweb.org/en/stable/"},
    "Bottle": {"desc": "Minimalist microframework for small web apps.", "doc": "https://bottlepy.org/docs/dev/"},
    "CherryPy": {"desc": "Object-oriented web framework with minimal setup.", "doc": "https://docs.cherrypy.dev/en/latest/"},
    "Pyramid": {"desc": "Flexible web framework for small to large apps.", "doc": "https://docs.pylonsproject.org/projects/pyramid/en/latest/"},
    "Sanic": {"desc": "Async web framework for speed and scalability.", "doc": "https://sanic.dev/en/"},
    "Falcon": {"desc": "Lightweight framework for high-performance APIs.", "doc": "https://falcon.readthedocs.io/en/stable/"},
    "Hug": {"desc": "Framework for creating simple, clean APIs.", "doc": "https://www.hug.rest/"},
    "Masonite": {"desc": "Modern web framework with Laravel-like syntax.", "doc": "https://docs.masoniteproject.com/"},
    "Dash": {"desc": "Framework for analytical web apps (built on Flask).", "doc": "https://dash.plotly.com/"},
    "Streamlit": {"desc": "Framework for data-driven web apps.", "doc": "https://docs.streamlit.io/"},
    "Tkinter": {"desc": "Standard Python GUI toolkit.", "doc": "https://docs.python.org/3/library/tkinter.html"},
    "PyQt": {"desc": "Python bindings for Qt (cross-platform GUI).", "doc": "https://www.riverbankcomputing.com/static/Docs/PyQt6/"},
    "PySide": {"desc": "Official Python bindings for Qt.", "doc": "https://doc.qt.io/qtforpython-6/"},
    "Kivy": {"desc": "Framework for cross-platform natural UIs.", "doc": "https://kivy.org/doc/stable/"},
    "wxPython": {"desc": "Python wrapper for wxWidgets GUI library.", "doc": "https://docs.wxpython.org/"},
    "PyGTK": {"desc": "Python bindings for GTK (Linux desktop apps).", "doc": "https://pygobject.readthedocs.io/en/latest/"},
    "Dear PyGui": {"desc": "Fast, GPU-accelerated GUI framework.", "doc": "https://dearpygui.readthedocs.io/en/latest/"},
    "Toga": {"desc": "Cross-platform GUI toolkit (BeeWare project).", "doc": "https://toga.readthedocs.io/en/latest/"},
    "Eel": {"desc": "Framework for GUI apps with web technologies.", "doc": "https://github.com/ChrisKnott/Eel#documentation"},
    "TensorFlow": {"desc": "Framework for machine learning.", "doc": "https://www.tensorflow.org/api_docs"},
    "PyTorch": {"desc": "Flexible deep learning framework.", "doc": "https://pytorch.org/docs/stable/index.html"},
    "Scikit-learn": {"desc": "ML library for classical algorithms.", "doc": "https://scikit-learn.org/stable/documentation.html"},
    "Keras": {"desc": "High-level API for neural networks.", "doc": "https://keras.io/api/"},
    "XGBoost": {"desc": "Optimized gradient boosting framework.", "doc": "https://xgboost.readthedocs.io/en/stable/"},
    "LightGBM": {"desc": "High-performance gradient boosting.", "doc": "https://lightgbm.readthedocs.io/en/latest/"},
    "CatBoost": {"desc": "Gradient boosting for categorical data.", "doc": "https://catboost.ai/en/docs/"},
    "Pandas": {"desc": "Data manipulation and analysis framework.", "doc": "https://pandas.pydata.org/docs/"},
    "NumPy": {"desc": "Fundamental framework for numerical computing.", "doc": "https://numpy.org/doc/stable/"},
    "SciPy": {"desc": "Framework for scientific computing.", "doc": "https://docs.scipy.org/doc/scipy/"},
    "Pytest": {"desc": "Powerful testing framework with plugins.", "doc": "https://docs.pytest.org/en/stable/"},
    "Unittest": {"desc": "Built-in Python testing framework.", "doc": "https://docs.python.org/3/library/unittest.html"},
    "Nose2": {"desc": "Successor to Nose testing framework.", "doc": "https://docs.nose2.io/en/latest/"},
    "Robot Framework": {"desc": "Keyword-driven test automation.", "doc": "https://robotframework.org/#documentation"},
    "Behave": {"desc": "Behavior-driven development framework.", "doc": "https://behave.readthedocs.io/en/stable/"},
    "Hypothesis": {"desc": "Property-based testing framework.", "doc": "https://hypothesis.readthedocs.io/en/latest/"},
    "Twisted": {"desc": "Event-driven networking framework.", "doc": "https://twistedmatrix.com/trac/wiki/Documentation"},
    "AIOHTTP": {"desc": "Async HTTP client/server framework.", "doc": "https://docs.aiohttp.org/en/stable/"},
    "Gevent": {"desc": "Coroutine-based concurrent networking.", "doc": "https://www.gevent.org/"},
    "Eventlet": {"desc": "Asynchronous framework for networking.", "doc": "https://eventlet.net/doc/"},
    "Pygame": {"desc": "Framework for 2D games and multimedia.", "doc": "https://www.pygame.org/docs/"},
    "Arcade": {"desc": "Modern Python framework for 2D games.", "doc": "https://api.arcade.academy/en/stable/"},
    "Pyglet": {"desc": "Lightweight framework for games.", "doc": "https://pyglet.readthedocs.io/en/latest/"},
    "Panda3D": {"desc": "3D game development framework.", "doc": "https://docs.panda3d.org/"},
    "SQLAlchemy": {"desc": "ORM framework for database interactions.", "doc": "https://docs.sqlalchemy.org/en/20/"},
    "Flask-RESTful": {"desc": "Extension of Flask for REST APIs.", "doc": "https://flask-restful.readthedocs.io/en/latest/"},
    "Celery": {"desc": "Distributed task queue framework.", "doc": "https://docs.celeryproject.org/en/stable/"},
    "Scrapy": {"desc": "Web scraping and crawling framework.", "doc": "https://docs.scrapy.org/en/latest/"},
    "Click": {"desc": "Framework for building CLI apps.", "doc": "https://click.palletsprojects.com/en/8.1.x/"},
    "Typer": {"desc": "Modern CLI framework with type hints.", "doc": "https://typer.tiangolo.com/"},
    "Jinja2": {"desc": "Templating engine for web frameworks.", "doc": "https://jinja.palletsprojects.com/en/3.1.x/"},
    "Matplotlib": {"desc": "Plotting and visualization framework.", "doc": "https://matplotlib.org/stable/contents.html"},
    "Seaborn": {"desc": "Statistical visualization framework.", "doc": "https://seaborn.pydata.org/"}
}

# Framework compatibility
incompatible_pairs = {
    ("Streamlit", "Django"): "Streamlit and Django are both web frameworks and typically not used together.",
    ("TensorFlow", "Tkinter"): "TensorFlow (ML) and Tkinter (GUI) serve different purposes and may not integrate directly."
}

# Example use cases
example_use_cases = {
    "Web App with Flask": {"frameworks": ["Flask"], "sections": ["Home", "About", "Contact"]},
    "ML Model with TensorFlow": {"frameworks": ["TensorFlow", "Pandas"], "sections": ["Data Prep", "Model", "Evaluation"]},
    "Desktop App with PyQt": {"frameworks": ["PyQt"], "sections": ["Main Window", "Settings", "Help"]}
}

# Framework selection with categories
st.subheader("Select Frameworks")
selected_frameworks = []
if selected_language == "Python":
    for category, framework_list in frameworks["Python"].items():
        with st.expander(category):
            selected = st.multiselect(f"Select {category} Frameworks", framework_list, key=category)
            selected_frameworks.extend(selected)
else:
    available_frameworks = frameworks.get(selected_language, frameworks["Python"]["Web Development"])
    selected_frameworks = st.multiselect("Select Frameworks", available_frameworks)

# Framework compatibility check
if len(selected_frameworks) > 1:
    for i, f1 in enumerate(selected_frameworks):
        for f2 in selected_frameworks[i+1:]:
            pair = tuple(sorted([f1, f2]))
            if pair in incompatible_pairs:
                st.warning(f"Compatibility Warning: {incompatible_pairs[pair]}")

# Display framework info with documentation links
if selected_frameworks:
    st.write("**Selected Frameworks Info:**")
    for framework in selected_frameworks:
        info = framework_info.get(framework, {"desc": "No description available.", "doc": None})
        desc = info["desc"]
        doc_link = f"[Documentation]({info['doc']})" if info["doc"] else "No documentation link available."
        st.write(f"- **{framework}:** {desc} {doc_link}")
else:
    st.write("**Selected Frameworks Info:** No frameworks selected yet.")

# Example use cases
st.subheader("Example Use Cases")
example_choice = st.selectbox("Select an Example (optional)", ["None"] + list(example_use_cases.keys()))
if example_choice != "None" and st.button("Apply Example"):
    example = example_use_cases[example_choice]
    selected_frameworks = example["frameworks"]
    st.session_state["selected_frameworks"] = selected_frameworks
    st.session_state["num_sections"] = len(example["sections"])
    st.session_state["section_names"] = example["sections"]
    st.success(f"Applied '{example_choice}' example!")

# Number of sections
num_sections = st.number_input("Number of Application Sections", min_value=1, max_value=20, value=st.session_state.get("num_sections", 1))

# Graphical Layout Designer
st.subheader("Design Your Layout")
layout_html = f"""
<div id="layout-container" style="width: 500px; height: 300px; border: 1px solid #ccc; position: relative; background: #f9f9f9;">
    {"".join([f'<div class="draggable" data-id="{i}" style="position: absolute; width: 100px; height: 50px; background: #e0e0e0; cursor: move; left: 10px; top: {i*60}px;">{section_names[i]}</div>' for i in range(num_sections)])}
</div>
<script>
    const container = document.getElementById('layout-container');
    const draggables = document.getElementsByClassName('draggable');
    let layoutData = [];

    function updateLayout() {{
        layoutData = [];
        for (let i = 0; i < draggables.length; i++) {{
            const rect = draggables[i].getBoundingClientRect();
            layoutData.push({{
                id: draggables[i].getAttribute('data-id'),
                x: rect.left - container.getBoundingClientRect().left,
                y: rect.top - container.getBoundingClientRect().top
            }});
        }}
        window.parent.postMessage({{type: 'layout_update', data: layoutData}}, '*');
    }}

    for (let i = 0; i < draggables.length; i++) {{
        draggables[i].addEventListener('mousedown', startDragging);
    }}

    function startDragging(e) {{
        const draggable = e.target;
        let shiftX = e.clientX - draggable.getBoundingClientRect().left;
        let shiftY = e.clientY - draggable.getBoundingClientRect().top;

        function moveAt(pageX, pageY) {{
            draggable.style.left = pageX - shiftX - container.getBoundingClientRect().left + 'px';
            draggable.style.top = pageY - shiftY - container.getBoundingClientRect().top + 'px';
        }}

        function onMouseMove(e) {{
            moveAt(e.pageX, e.pageY);
        }}

        document.addEventListener('mousemove', onMouseMove);

        document.onmouseup = function() {{
            document.removeEventListener('mousemove', onMouseMove);
            document.onmouseup = null;
            updateLayout();
        }};
    }}

    document.addEventListener('dragstart', (e) => e.preventDefault());
</script>
"""
components.html(layout_html, height=320, scrolling=True)
if st.button("Save Layout"):
    # Placeholder: Ideally, this would capture layout_data from JS, but requires additional bridging
    st.session_state["layout_data"] = [{"id": i, "x": 10, "y": i*60} for i in range(num_sections)]
layout_data = st.session_state.get("layout_data", [{"id": i, "x": 10, "y": i*60} for i in range(num_sections)])

# Section names input - Fixed to avoid IndexError
if "section_names" not in st.session_state or len(st.session_state["section_names"]) != num_sections:
    st.session_state["section_names"] = [f"Section{i+1}" for i in range(num_sections)]
section_names = st.session_state["section_names"]
for i in range(num_sections):
    section_names[i] = st.text_input(f"Name of Section {i+1}", value=section_names[i], key=f"section_{i}")
st.session_state["section_names"] = section_names

# Generate button
if st.button("Generate"):
    if not api_key:
        st.error("Please enter a valid API Key")
    elif not selected_frameworks:
        st.error("Please select at least one framework")
    else:
        frameworks_str = ", ".join(selected_frameworks)
        layout_str = "custom layout with positions: " + ", ".join([f"{n} at ({d['x']},{d['y']})" for n, d in zip(section_names, layout_data)]) if layout_data else "default layout"
        prompt = f"""Generate boilerplate code for a {selected_language} application 
        using the following frameworks: {frameworks_str}. The application should have 
        {num_sections} sections named: {', '.join(section_names)}. Arrange the sections 
        in a {layout_str}. Include basic structure and comments for each section, 
        integrating the selected frameworks appropriately."""

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        data = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            generated_code = result["candidates"][0]["content"]["parts"][0]["text"]
            st.subheader("Generated Code")
            st.code(generated_code, language=selected_language.lower())
            st.download_button(
                label="Download Generated Code",
                data=generated_code,
                file_name=f"generated_gui_{selected_language.lower()}.txt",
                mime="text/plain"
            )
        except requests.exceptions.RequestException as e:
            st.error(f"Error calling the API: {str(e)}")
        except (KeyError, IndexError) as e:
            st.error("Error parsing API response. Please check your API key and try again.")

# Add some basic instructions
st.sidebar.header("Instructions")
st.sidebar.write("""
1. Enter your Google AI Studio API Key
2. Select your preferred programming language
3. Choose frameworks from the categories
4. Optionally apply an example use case
5. Drag sections in the layout designer and save
6. Name your sections
7. Click 'Generate' to create your boilerplate code
""")
