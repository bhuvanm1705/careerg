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
    """Generate a dynamic career plan using DeepSeek API based on user inputs."""
    prompt = (
        f"You are a highly knowledgeable career advisor. Create a detailed, actionable career plan "
        f"tailored to the following user inputs:\n"
        f"- Engineering Education: {education}\n"
        f"- Skills: {skills}\n"
        f"- Internships/Experience: {internships}\n"
        f"- Interests: {interests}\n"
        f"- Career Goals: {goals}\n\n"
        f"Structure the plan as follows:\n"
        f"1. Short-term steps (1-2 years): Specific actions to build on their skills and experience.\n"
        f"2. Long-term steps (3-5 years): Steps to achieve their career goals.\n"
        f"3. Job roles to target: Relevant positions based on their profile.\n"
        f"4. Skills to learn: New skills to acquire for success.\n"
        f"5. Resources: Recommended courses, books, or tools (be specific).\n"
        f"Ensure the plan is concise, practical, and directly reflects the user's inputs."
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",  # DeepSeek-V3 for general-purpose responses
            messages=[
                {"role": "system", "content": "You are a career advisor with expertise across all fields."},
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
    gr.Markdown("Enter your details below to get a personalized career plan tailored to your inputs.")
    
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