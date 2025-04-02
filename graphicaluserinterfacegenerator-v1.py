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

# Frameworks dropdown (some examples for different languages)
frameworks = {
    "Python": ["Django", "Flask", "PyQt", "Tkinter", "Streamlit"],
    "JavaScript": ["React", "Vue.js", "Angular", "Node.js", "Express"],
    "Java": ["Spring", "JavaFX", "Swing", "JSF", "Vaadin"],
    "C++": ["Qt", "wxWidgets", "FLTK", "GTK+"],
    "C#": [".NET", "WPF", "Windows Forms", "Xamarin"]
}
# Filter frameworks based on selected language (default to Python if language not in dict)
available_frameworks = frameworks.get(selected_language, frameworks["Python"])
selected_framework = st.selectbox("Select Framework", available_frameworks)

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
