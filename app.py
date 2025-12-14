import streamlit as st
import os
import google.generativeai as genai

# --- 1. Streamlit Configuration and Secret Management ---

# Set up page config
st.set_page_config(page_title="Career Guidance Chatbot", layout="wide")
st.title("Career Guidance Chatbot")
st.markdown("Enter your details to get a personalized career plan powered by Google Gemini.")
st.markdown("---")

# Safely get the GOOGLE_API_KEY from Streamlit Secrets
# The key must be defined in your Streamlit secrets file (see Step 3)
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("Error: GOOGLE_API_KEY not found in Streamlit secrets.")
    st.markdown("Please configure the key in the Streamlit cloud settings or a local `.streamlit/secrets.toml` file.")
    st.stop()

# Configure the Google Generative AI client
genai.configure(api_key=API_KEY)

# --- 2. Core Logic Function (Reused from Gradio App) ---

def generate_career_plan(education, skills, internships, interests):
    """Generate a dynamic career plan using Google Gemini API."""
    
    # Construct the detailed prompt
    prompt = (
        f"You are a highly knowledgeable career advisor. Create a detailed, actionable career plan "
        f"tailored to the following user inputs:\n"
        f"- Engineering Education: {education}\n"
        f"- Skills: {skills}\n"
        f"- Internships/Experience: {internships}\n"
        f"- Interests: {interests}\n\n"
        f"Structure the plan as follows:\n"
        f"1. Short-term steps : Break this section down into:\n"
        f"   a. Immediate actions (0–3 months): Quick wins or high-impact tasks based on their current skills.\n"
        f"   b. Mid-term steps (5–8 months): Actions to deepen expertise, expand network, or build relevant experience.\n"
        f"   c. Longer short-term (1–2 years): Projects, certifications, or job transitions to solidify the foundation.\n"
        f"2. Long-term steps (3–5 years): Steps to advance their career based on interests and background.\n"
        f"3. Job roles to target: Relevant positions based on their profile.\n"
        f"4. Skills to learn: New skills to acquire for success.\n"
        f"5. Resources: Recommended courses, books, or tools (be specific).\n"
        f"Ensure the plan is concise, practical, and directly reflects the user's inputs."
    )

    try:
        # Initialize the Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")  # Reusing model name
        response = model.generate_content(prompt)
        
        # Check if response is valid
        if not response.text:
            return "Error: No response generated. Check API key or model availability."
        
        # Return the generated plan as a string
        return response.text
    
    except Exception as e:
        return f"Error: {str(e)}. Check your API key or network connection."

# --- 3. Streamlit UI Implementation ---

# Create columns for input and output, similar to your gr.Row()
col1, col2 = st.columns(2)

with col1:
    # Use st.text_area for multi-line inputs, st.text_input for single lines
    education = st.text_input(label="Engineering Education (e.g., Computer Science, Mechanical)")
    skills = st.text_area(label="Skills (e.g., Python, CAD, project management)")
    internships = st.text_area(label="Internships/Experience (e.g., 3 months at XYZ Corp)")
    interests = st.text_area(label="Interests (e.g., AI, robotics, sustainable energy)")
    
    # Streamlit button
    submit_btn = st.button("Generate Career Plan", type="primary")

with col2:
    st.subheader("Your Personalized Career Plan")
    # Placeholder for the output
    output_placeholder = st.empty()

# --- 4. Streamlit Action Logic ---

if submit_btn:
    # Check if essential fields are filled
    if not all([education, skills, internships, interests]):
        output_placeholder.warning("Please fill in all the input fields to generate the plan.")
    else:
        # Use a spinner while the API call is running
        with st.spinner("Generating plan... This may take up to 10 seconds."):
            plan = generate_career_plan(education, skills, internships, interests)
            
            # Display the result in the output column
            output_placeholder.markdown(plan)

# Optional: Add a note at the end
st.markdown("---")
st.caption("Powered by Google Gemini and Streamlit.")
