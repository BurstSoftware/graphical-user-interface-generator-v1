# graphicaluserinterfacegeneratorv1.py
import streamlit as st
import requests
import json

# Title of the application
st.title("Graphical User Interface Generator")

# API Key input
api_key = st.text_input("Enter your Google AI Studio API Key", type="password")

# Programming languages dropdown
programming_languages = [
    "Python", "JavaScript", "Java", "C++", "C#", "Ruby", "PHP", "TypeScript",
    "Swift", "Kotlin", "Go", "Rust", "Scala", "Perl", "R"
]
selected_language = st.selectbox("Select Programming Language", programming_languages)

# Frameworks dictionary with descriptions
frameworks = {
    "Python": [
        # Web Development Frameworks
        "Django", "Flask", "FastAPI", "Tornado", "Bottle", "CherryPy", "Pyramid", 
        "Sanic", "Falcon", "Hug", "Masonite", "Dash", "Streamlit",
        # GUI Frameworks
        "Tkinter", "PyQt", "PySide", "Kivy", "wxPython", "PyGTK", "Dear PyGui", 
        "Toga", "Eel",
        # Machine Learning and Data Science Frameworks
        "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "XGBoost", "LightGBM", 
        "CatBoost", "Pandas", "NumPy", "SciPy",
        # Testing Frameworks
        "Pytest", "Unittest", "Nose2", "Robot Framework", "Behave", "Hypothesis",
        # Networking and Asynchronous Frameworks
        "Twisted", "AIOHTTP", "Gevent", "Eventlet",
        # Game Development Frameworks
        "Pygame", "Arcade", "Pyglet", "Panda3D",
        # Other Notable Frameworks
        "SQLAlchemy", "Flask-RESTful", "Celery", "Scrapy", "Click", "Typer", 
        "Jinja2", "Matplotlib", "Seaborn"
    ],
    "JavaScript": ["React", "Vue.js", "Angular", "Node.js", "Express"],
    "Java": ["Spring", "JavaFX", "Swing", "JSF", "Vaadin"],
    "C++": ["Qt", "wxWidgets", "FLTK", "GTK+"],
    "C#": [".NET", "WPF", "Windows Forms", "Xamarin"]
}

# Framework descriptions
framework_descriptions = {
    # Web Development Frameworks
    "Django": "High-level web framework for rapid development with a 'batteries-included' philosophy.",
    "Flask": "Lightweight microframework for building web applications with flexibility.",
    "FastAPI": "Modern, high-performance web framework for building APIs with async support.",
    "Tornado": "Asynchronous web framework and networking library for handling thousands of connections.",
    "Bottle": "Minimalist microframework for small web applications.",
    "CherryPy": "Object-oriented web framework for building web apps with minimal setup.",
    "Pyramid": "Flexible web framework that scales from small to large applications.",
    "Sanic": "Async web framework designed for speed and scalability.",
    "Falcon": "Lightweight framework for building high-performance APIs.",
    "Hug": "Framework for creating simple, clean APIs with automatic documentation.",
    "Masonite": "Modern web framework with a Laravel-like syntax.",
    "Dash": "Framework for building analytical web applications (built on Flask).",
    "Streamlit": "Framework for creating data-driven web apps with minimal code (used in this project!).",
    # GUI Frameworks
    "Tkinter": "Standard Python GUI toolkit included with Python.",
    "PyQt": "Python bindings for the Qt framework (cross-platform GUI development).",
    "PySide": "Official Python bindings for Qt, alternative to PyQt.",
    "Kivy": "Framework for building cross-platform applications with natural user interfaces.",
    "wxPython": "Python wrapper for the wxWidgets C++ library for GUIs.",
    "PyGTK": "Python bindings for GTK, popular for Linux desktop applications.",
    "Dear PyGui": "Fast, GPU-accelerated GUI framework for real-time applications.",
    "Toga": "Cross-platform GUI toolkit for desktop and mobile apps (part of the BeeWare project).",
    "Eel": "Framework for building simple GUI apps with web technologies (HTML/CSS/JS).",
    # Machine Learning and Data Science Frameworks
    "TensorFlow": "Open-source framework for machine learning and deep learning.",
    "PyTorch": "Flexible deep learning framework with dynamic computation graphs.",
    "Scikit-learn": "Machine learning library for classical algorithms and data preprocessing.",
    "Keras": "High-level API for building neural networks (often used with TensorFlow).",
    "XGBoost": "Optimized gradient boosting framework for machine learning.",
    "LightGBM": "High-performance gradient boosting framework.",
    "CatBoost": "Gradient boosting framework optimized for categorical data.",
    "Pandas": "Data manipulation and analysis framework (not strictly ML but foundational).",
    "NumPy": "Fundamental framework for numerical computing in Python.",
    "SciPy": "Framework for scientific and technical computing.",
    # Testing Frameworks
    "Pytest": "Powerful testing framework with simple syntax and extensive plugins.",
    "Unittest": "Built-in Python testing framework for unit tests.",
    "Nose2": "Successor to Nose, a testing framework with plugin support.",
    "Robot Framework": "Keyword-driven test automation framework.",
    "Behave": "Behavior-driven development (BDD) framework for Python.",
    "Hypothesis": "Property-based testing framework for Python.",
    # Networking and Asynchronous Frameworks
    "Twisted": "Event-driven networking framework for building servers and clients.",
    "AIOHTTP": "Asynchronous HTTP client/server framework built on asyncio.",
    "Gevent": "Coroutine-based framework for concurrent networking.",
    "Eventlet": "Asynchronous framework for networking and concurrency.",
    # Game Development Frameworks
    "Pygame": "Framework for building 2D games and multimedia applications.",
    "Arcade": "Modern Python framework for 2D game development.",
    "Pyglet": "Lightweight framework for games and multimedia without external dependencies.",
    "Panda3D": "3D game development framework for Python (and C++).",
    # Other Notable Frameworks
    "SQLAlchemy": "ORM (Object-Relational Mapping) framework for database interactions.",
    "Flask-RESTful": "Extension of Flask for building REST APIs.",
    "Celery": "Distributed task queue framework for background processing.",
    "Scrapy": "Web scraping and crawling framework.",
    "Click": "Framework for building command-line interfaces (CLI).",
    "Typer": "Modern CLI framework built on Click with type hints.",
    "Jinja2": "Templating engine often used with web frameworks like Flask.",
    "Matplotlib": "Plotting and visualization framework for data science.",
    "Seaborn": "Statistical data visualization framework (built on Matplotlib)."
}

# Filter frameworks based on selected language (default to Python if language not in dict)
available_frameworks = frameworks.get(selected_language, frameworks["Python"])
selected_framework = st.selectbox("Select Framework", available_frameworks)

# Display framework description
framework_description = framework_descriptions.get(selected_framework, "No description available.")
st.write(f"**Framework Description:** {framework_description}")

# Number of sections
num_sections = st.number_input("Number of Application Sections", min_value=1, max_value=20, value=1)

# Section names input
section_names = []
for i in range(num_sections):
    section_name = st.text_input(f"Name of Section {i+1}", value=f"Section{i+1}")
    section_names.append(section_name)

# Generate button
if st.button("Generate"):
    if not api_key:
        st.error("Please enter a valid API Key")
    else:
        # Construct the prompt for the API
        prompt = f"""Generate boilerplate code for a {selected_language} application 
        using the {selected_framework} framework. The application should have 
        {num_sections} sections named: {', '.join(section_names)}. 
        Include basic structure and comments for each section."""

        # API call setup
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        try:
            # Make the API call
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            generated_code = result["candidates"][0]["content"]["parts"][0]["text"]
            
            # Display the generated code
            st.subheader("Generated Code")
            st.code(generated_code, language=selected_language.lower())
            
            # Provide download button
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
3. Choose a framework
4. Specify the number of sections
5. Name each section
6. Click 'Generate' to create your boilerplate code
""")
