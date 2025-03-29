import os
import requests
import gradio as gr
from datetime import datetime

# Set up NASA API key from environment variable
API_KEY = os.getenv("NASA_API_KEY", "DEMO_KEY")  # Default to DEMO_KEY if not set
BASE_URL = "https://api.nasa.gov/planetary/apod"

def generate_career_plan(education, skills, internships, interests, goals):
    """Generate a career plan with NASA APOD data for space-related inspiration."""
    # Fetch APOD data for inspiration
    try:
        response = requests.get(
            BASE_URL,
            params={"api_key": API_KEY, "date": datetime.now().strftime("%Y-%m-%d")}
        )
        response.raise_for_status()
        apod_data = response.json()
        apod_title = apod_data.get("title", "Astronomy Picture of the Day")
        apod_explanation = apod_data.get("explanation", "No explanation available.")
        apod_url = apod_data.get("url", "No image available.")
    except requests.exceptions.RequestException as e:
        apod_title = "Error fetching APOD"
        apod_explanation = f"Could not fetch NASA data: {str(e)}"
        apod_url = "N/A"

    # Check if the user's interests or goals are space-related
    space_related = any(keyword in (interests + goals).lower() for keyword in 
                        ["space", "aerospace", "astronomy", "nasa", "astro", "planetary", "mars"])

    # Generate a career plan
    career_plan = f"### Your Personalized Career Plan\n\n"
    career_plan += f"**Education**: {education}\n"
    career_plan += f"**Skills**: {skills}\n"
    career_plan += f"**Internships/Experience**: {internships}\n"
    career_plan += f"**Interests**: {interests}\n"
    career_plan += f"**Career Goals**: {goals}\n\n"

    career_plan += "#### 1. Short-term Steps (1-2 Years)\n"
    career_plan += f"- Enhance your {skills} with projects (e.g., analyze NASA datasets).\n"
    career_plan += "- Take online courses like 'Introduction to Aerospace Engineering' on Coursera.\n"
    if space_related:
        career_plan += "- Explore NASA internships (e.g., NASA Pathways Program).\n"
    else:
        career_plan += f"- Seek internships in {interests}-related fields.\n"

    career_plan += "\n#### 2. Long-term Steps (3-5 Years)\n"
    if space_related:
        career_plan += "- Aim for a role at NASA or a space company (e.g., SpaceX).\n"
        career_plan += "- Contribute to space-related open-source projects.\n"
    else:
        career_plan += f"- Pursue a career in {goals.split(',')[0].strip()}.\n"
    career_plan += "- Consider a master’s degree if relevant to your goals.\n"

    career_plan += "\n#### 3. Job Roles to Target\n"
    if space_related:
        career_plan += "- Aerospace Engineer\n- Data Scientist (Space Division)\n"
    else:
        career_plan += f"- Roles aligned with {interests} (e.g., Engineer, Analyst)\n"

    career_plan += "\n#### 4. Skills to Learn\n"
    career_plan += f"- Advanced {skills.split(',')[0].strip()} techniques\n"
    if space_related:
        career_plan += "- Space mission analysis tools (e.g., STK)\n"

    career_plan += "\n#### 5. Resources\n"
    career_plan += "- **Courses**: 'Space Mission Design' on edX\n"
    career_plan += "- **Books**: 'Introduction to Space Flight' by Francis J. Hale\n"
    if space_related:
        career_plan += "- **NASA API**: Explore more at [api.nasa.gov](https://api.nasa.gov)\n"

    # Add NASA APOD inspiration
    career_plan += "\n#### Space Inspiration from NASA\n"
    career_plan += f"**{apod_title}**\n"
    career_plan += f"{apod_explanation}\n"
    career_plan += f"View the image: [{apod_url}]({apod_url})\n"

    return career_plan

# Gradio interface
with gr.Blocks(title="Career Guidance Chatbot") as demo:
    gr.Markdown("# Career Guidance Chatbot")
    gr.Markdown("Enter your details below to get a personalized career plan with NASA space inspiration.")
    
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