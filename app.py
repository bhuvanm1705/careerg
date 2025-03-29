import os
from openai import OpenAI
import gradio as gr

# Set up DeepSeek API key from environment variable
API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not API_KEY:
    raise ValueError("DEEPSEEK_API_KEY not set. Add it in Hugging Face Space Secrets.")

# Initialize OpenAI client with DeepSeek's base URL
client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.deepseek.com"
)

def generate_career_plan(education, skills, internships, interests, goals):
    """Generate a career plan using DeepSeek API."""
    prompt = (
        f"As a career advisor, provide a detailed career plan for a student with:\n"
        f"- Engineering Education: {education}\n"
        f"- Skills: {skills}\n"
        f"- Internships/Experience: {internships}\n"
        f"- Interests: {interests}\n"
        f"- Career Goals: {goals}\n\n"
        f"Include:\n"
        f"1. Short-term steps (1-2 years)\n"
        f"2. Long-term steps (3-5 years)\n"
        f"3. Job roles to target\n"
        f"4. Skills to learn\n"
        f"5. Resources (courses, books, etc.)\n"
        f"Keep it concise, actionable, and tailored."
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # Use DeepSeek-V3 model
            messages=[
                {"role": "system", "content": "You are a highly knowledgeable career advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}. Check your API key or try again later."

# Gradio interface
with gr.Blocks(title="Career Guidance Chatbot") as demo:
    gr.Markdown("# Career Guidance Chatbot")
    gr.Markdown("Enter your details below to get a personalized career plan powered by DeepSeek.")
    
    with gr.Row():
        with gr.Column():
            education = gr.Textbox(label="Engineering Education (e.g., Computer Science, Mechanical)")
            skills = gr.Textbox(label="Skills (e.g., Python, CAD, project management)")
            internships = gr.Textbox(label="Internships/Experience (e.g., 3 months at XYZ Corp)")
            interests = gr.Textbox(label="Interests (e.g., AI, robotics, sustainable energy)")
            goals = gr.Textbox(label="Career Goals (e.g., become a data scientist)")
            submit_btn = gr.Button("Generate Career Plan")
        
        with gr.Column():
            output = gr.Markdown(label="Your Career Plan")
    
    submit_btn.click(
        fn=generate_career_plan,
        inputs=[education, skills, internships, interests, goals],
        outputs=output
    )

# Launch the app
demo.launch()