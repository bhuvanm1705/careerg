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
    prompt = (
        f"You are a highly knowledgeable career advisor. Create a detailed, actionable career plan "
        f"tailored to the following user inputs:\n"
        f"- Engineering Education: {education}\n"
        f"- Skills: {skills}\n"
        f"- Internships/Experience: {internships}\n"
        f"- Interests: {interests}\n\n"
        f"Structure the plan as follows:\n"
        f"   a. Immediate actions (0–3 months)\n"
        f"   b. Mid-term steps (5–8 months)\n"
        f"   c. Longer short-term (1–2 years)\n"
        f"2. Long-term steps (3–5 years)\n"
        f"3. Job roles to target\n"
        f"4. Skills to learn\n"
        f"5. Resources (specific courses, books, tools)\n"
    )

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return "", response.text if response.text else "Error: No response generated."
    except Exception as e:
        return "", f"Error: {str(e)}. Check your API key or network connection."

with gr.Blocks(title="Career Guidance Chatbot") as demo:
    gr.Markdown("# 💼 Career Guidance Chatbot")
    gr.Markdown("Fill in your background to get a personalized career development plan using Google Gemini.")

    with gr.Row():
        with gr.Column():
            education = gr.Textbox(label="🎓 Engineering Education")
            skills = gr.Textbox(label="🛠️ Skills")
            internships = gr.Textbox(label="💼 Internships/Experience")
            interests = gr.Textbox(label="🌟 Interests")
            submit_btn = gr.Button("🚀 Generate Career Plan")

        with gr.Column():
            status = gr.Markdown("⏳ Waiting for input...", visible=True)
            output = gr.Markdown("")

    def run_with_status(*args):
        return "⏳ Generating your personalized career plan...", *generate_career_plan(*args)

    submit_btn.click(
        fn=run_with_status,
        inputs=[education, skills, internships, interests],
        outputs=[status, output]
    )

demo.launch()
