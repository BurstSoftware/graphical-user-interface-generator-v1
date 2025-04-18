# graphicaluserinterfacegeneratorv1.py
import streamlit as st
import requests
import json

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

# Framework descriptions and documentation links
framework_info = {
    "Django": {"desc": "High-level web framework for rapid development.", "doc": "https://docs.djangoproject.com/"},
    "Flask": {"desc": "Lightweight microframework for web apps.", "doc": "https://flask.palletsprojects.com/"},
    "FastAPI": {"desc": "High-performance API framework with async support.", "doc": "https://fastapi.tiangolo.com/"},
    "Streamlit": {"desc": "Framework for data-driven web apps.", "doc": "https://docs.streamlit.io/"},
    "Tkinter": {"desc": "Standard Python GUI toolkit.", "doc": "https://docs.python.org/3/library/tkinter.html"},
    "PyQt": {"desc": "Python bindings for Qt (cross-platform GUI).", "doc": "https://www.riverbankcomputing.com/static/Docs/PyQt5/"},
    "TensorFlow": {"desc": "Framework for machine learning.", "doc": "https://www.tensorflow.org/api_docs"},
    "PyTorch": {"desc": "Flexible deep learning framework.", "doc": "https://pytorch.org/docs/stable/index.html"},
    "Pandas": {"desc": "Data manipulation and analysis framework.", "doc": "https://pandas.pydata.org/docs/"},
    # Add more as needed; for brevity, not all are included here
}

# Framework compatibility (example conflicts)
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

# Number of sections (with session state for example use cases)
num_sections = st.number_input("Number of Application Sections", min_value=1, max_value=20, value=st.session_state.get("num_sections", 1))

# Visual Layout Designer (text-based)
st.subheader("Design Your Layout")
layout_options = ["Vertical Stack", "Horizontal Row", "Grid (2 columns)", "Tabs"]
layout_choice = st.selectbox("Select Layout Style", layout_options)
layout_desc = {
    "Vertical Stack": "Sections stacked vertically.",
    "Horizontal Row": "Sections side by side horizontally.",
    "Grid (2 columns)": "Sections in a 2-column grid.",
    "Tabs": "Sections as separate tabs."
}
st.write(f"**Layout Description:** {layout_desc[layout_choice]}")

# Section names input (with session state for example use cases)
section_names = st.session_state.get("section_names", [f"Section{i+1}" for i in range(num_sections)])
for i in range(num_sections):
    section_names[i] = st.text_input(f"Name of Section {i+1}", value=section_names[i], key=f"section_{i}")
st.session_state["section_names"] = section_names[:num_sections]

# Generate button
if st.button("Generate"):
    if not api_key:
        st.error("Please enter a valid API Key")
    elif not selected_frameworks:
        st.error("Please select at least one framework")
    else:
        frameworks_str = ", ".join(selected_frameworks)
        prompt = f"""Generate boilerplate code for a {selected_language} application 
        using the following frameworks: {frameworks_str}. The application should have 
        {num_sections} sections named: {', '.join(section_names)}. Arrange the sections 
        in a {layout_choice.lower()} layout. Include basic structure and comments for 
        each section, integrating the selected frameworks appropriately."""

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
5. Design your layout and name sections
6. Click 'Generate' to create your boilerplate code
""")
