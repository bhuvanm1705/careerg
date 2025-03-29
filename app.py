import gradio as gr
from huggingface_hub import InferenceClient

import os
from openai import OpenAI


# Set up OpenAI API key (to be provided via Hugging Face Secrets)
API_KEY = os.getenv("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")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set. Please add it in the Space's Secrets settings.")
client = OpenAI(api_key=API_KEY)

def generate_career_plan(education, skills, internships, interests, goals):
    """Generate a career plan using OpenAI API."""
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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a highly knowledgeable career advisor."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7,
            top_p=1.0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}. Check your API key or network connection."

# Gradio interface
with gr.Blocks(title="Career Guidance Chatbot") as demo:
    gr.Markdown("# Career Guidance Chatbot")
    gr.Markdown("Enter your details below to get a personalized career plan powered by OpenAI.")
    
    with gr.Row():
        with gr.Column():
            education = gr.Textbox(label="Engineering Education (e.g., Computer Science, Mechanical)")
            skills = gr.Textbox(label="Skills (e.g., Python, CAD, project management)")
            internships = gr.Textbox(label="Internships/Experience (e.g., 3 months at XYZ Corp, software dev)")
            interests = gr.Textbox(label="Interests (e.g., AI, robotics, sustainable energy)")
            goals = gr.Textbox(label="Career Goals (e.g., become a data scientist, start a tech company)")
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