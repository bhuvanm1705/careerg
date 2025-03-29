import os
import http.client
import gradio as gr
import json

# Set up RapidAPI key from environment variable
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_KEY not set. Add it in Hugging Face Space Secrets.")

def generate_career_plan(education, skills, internships, interests, goals):
    """Generate a dynamic career plan using Infinite GPT API."""
    # Construct the prompt
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

    # Set up the HTTP connection to Infinite GPT API
    conn = http.client.HTTPSConnection("infinite-gpt.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "infinite-gpt.p.rapidapi.com",
        'Content-Type': "application/json"
    }
    payload = json.dumps({"query": prompt, "sysMsg": "You are a friendly and expert career advisor."})

    try:
        # Make the POST request
        conn.request("POST", "/infinite-gpt", payload, headers)
        res = conn.getresponse()
        
        # Check if the response is successful
        if res.status != 200:
            return f"Error: API request failed with status {res.status} - {res.reason}"
        
        # Decode and parse the response
        data = res.read().decode("utf-8")
        try:
            response_json = json.loads(data)
            # Assuming the API returns the generated text in a 'response' field (adjust based on actual API spec)
            career_plan = response_json.get("response", "Error: No response field in API output")
            return career_plan
        except json.JSONDecodeError:
            return f"Error: Invalid JSON response from API - {data}"
    except Exception as e:
        return f"Error: {str(e)}. Check your API key or network connection."
    finally:
        conn.close()

# Gradio interface
with gr.Blocks(title="Career Guidance Chatbot") as demo:
    gr.Markdown("# Career Guidance Chatbot")
    gr.Markdown("Enter your details below to get a personalized career plan powered by Infinite GPT.")
    
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