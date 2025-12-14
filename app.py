import streamlit as st
import os
# Import only the Groq SDK
from groq import Groq 

# --- 1. Streamlit Configuration and Secret Management ---

st.set_page_config(page_title="Career Guidance Chatbot (Powered by Groq)", layout="wide")
st.title("Career Guidance Chatbot")
st.markdown("Enter your details to get a personalized career plan powered by **Groq**. 🚀")
st.markdown("---")

# Safely get the GROQ_API_KEY from Streamlit Secrets
try:
    API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Error: GROQ_API_KEY not found in Streamlit secrets.")
    st.markdown("Please configure the key in the Streamlit cloud settings as `GROQ_API_KEY`.")
    st.stop()

# Configure the Groq client only
client = Groq(api_key=API_KEY) # Initialize Groq Client

# --- 2. Core Logic Function (Updated for Groq) ---

def generate_career_plan(education, skills, internships, interests):
    """Generate a dynamic career plan using the Groq API."""
    
    prompt = (
        f"You are a highly knowledgeable career advisor. Create a detailed, actionable career plan "
        f"tailored to the following user inputs:\n"
        f"- Engineering Education: {education}\n"
        f"- Skills: {skills}\n"
        f"- Internships/Experience: {internships}\n"
        f"- Interests: {interests}\n\n"
        f"Structure the plan as follows:\n"
        f"1. Short-term steps: Break this section down into:\n"
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
        # Call the Groq Chat Completions API
        chat_completion = client.chat.completions.create(
            # Using a fast, high-performance Groq model
            model="llama3-70b-8192", 
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        
        response_text = chat_completion.choices[0].message.content
        
        if not response_text:
            return "Error: No response generated. Check API key or model availability."
        
        return response_text
    
    except Exception as e:
        return f"Error: {str(e)}. Check your API key or network connection."

# --- 3. Streamlit UI Implementation (No Changes Needed) ---

col1, col2 = st.columns(2)

with col1:
    education = st.text_input(label="Engineering Education (e.g., Computer Science, Mechanical)")
    skills = st.text_area(label="Skills (e.g., Python, CAD, project management)")
    internships = st.text_area(label="Internships/Experience (e.g., 3 months at XYZ Corp)")
    interests = st.text_area(label="Interests (e.g., AI, robotics, sustainable energy)")
    submit_btn = st.button("Generate Career Plan", type="primary")

with col2:
    st.subheader("Your Personalized Career Plan")
    output_placeholder = st.empty()

# --- 4. Streamlit Action Logic (Updated Spinner Text) ---

if submit_btn:
    if not all([education, skills, internships, interests]):
        output_placeholder.warning("Please fill in all the input fields to generate the plan.")
    else:
        with st.spinner("Generating plan... This will be super fast! 🚀"):
            plan = generate_career_plan(education, skills, internships, interests)
            output_placeholder.markdown(plan)

st.markdown("---")
st.caption("Powered by Groq and Streamlit.")
