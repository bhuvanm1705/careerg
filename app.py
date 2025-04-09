import os
import google.generativeai as genai
import gradio as gr

# Set up Google API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not set. Add it in Hugging Face Space Secrets.")

# Configure the Google Generative AI client
genai.configure(api_key=API_KEY)

def generate_career_plan(education, skills, internships, interests):
    """Generate a dynamic career plan using Google Gemini API without career goals."""
    # Construct the prompt without career goals
    prompt = (
    f"You are a highly knowledgeable career advisor. Create a detailed, actionable career plan "
    f"tailored to the following user inputs:\n"
    f"- Engineering Education: {education}\n"
    f"- Skills: {skills}\n"
    f"- Internships/Experience: {internships}\n"
    f"- Interests: {interests}\n\n"
    f"Structure the plan as follows:\n"
    f"1. Short-term steps (1-2 years): Break this section down into:\n"
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
        model = genai.GenerativeModel("gemini-1.5-flash")  # Adjust model name if needed
        response = model.generate_content(prompt)
        
        # Check if response is valid
        if not response.text:
            return "Error: No response generated. Check API key or model availability."
        return response.text
    except Exception as e:
        return f"Error: {str(e)}. Check your API key or network connection."

# Gradio interface without Career Goals
with gr.Blocks(title="Career Guidance Chatbot") as demo:
    gr.Markdown("# Career Guidance Chatbot")
    gr.Markdown("Enter your details to get a personalized career plan powered by Google Gemini.")
    
    with gr.Row():
        with gr.Column():
            education = gr.Textbox(label="Engineering Education (e.g., Computer Science, Mechanical)")
            skills = gr.Textbox(label="Skills (e.g., Python, CAD, project management)")
            internships = gr.Textbox(label="Internships/Experience (e.g., 3 months at XYZ Corp)")
            interests = gr.Textbox(label="Interests (e.g., AI, robotics, sustainable energy)")
            submit_btn = gr.Button("Generate Career Plan")
        
        with gr.Column():
            output = gr.Markdown(label="Your Career Plan")
    
    submit_btn.click(
        fn=generate_career_plan,
        inputs=[education, skills, internships, interests],
        outputs=output
    )

# Launch the app
demo.launch()