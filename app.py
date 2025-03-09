import os
from flask import Flask, request, jsonify
import openai

# -------------------------------
# FLASK APP SETUP
# -------------------------------
app = Flask(__name__)

# Configuration
app.config["SECRET_KEY"] = "1234"

# Set OpenAI API key from environment variable.
# Make sure you set OPENAI_API_KEY in Vercel’s Environment Variables.
openai.api_key = os.environ.get("OPENAI_API_KEY")

# -------------------------------
# FLASK ROUTES
# -------------------------------

@app.route("/")
def index():
    return "Hello from Flask! This is your Roadmap Planner Chatbot."

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    """
    This route accepts a POST request with JSON body: { "prompt": "your text" }.
    It calls the OpenAI API and returns a generated roadmap.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"roadmap": "Error: No valid JSON body provided."}), 400

    prompt = data.get("prompt", "")
    try:
        # Check if API key is set; if not, raise an error.
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set. Please set it as an environment variable.")
        
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.5
        )
        generated_text = response.choices[0].text.strip()
    except Exception as e:
        generated_text = f"Error generating plan: {str(e)}"
    
    return jsonify({"roadmap": generated_text})

@app.route("/fetch-resources", methods=["POST"])
def fetch_resources():
    """
    This route accepts a POST request with JSON body: { "category": "Technology" }.
    It returns a list of sample learning resources.
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"resources": ["Error: No valid JSON body provided."]}), 400

    category = data.get("category", "")
    resources = {
        "Technology": ["Coursera - Python for Everybody", "Udemy - Web Dev Bootcamp"],
        "Business": ["edX - Business Foundations", "LinkedIn Learning - Marketing Strategies"],
        "Creative Arts": ["Skillshare - Graphic Design Basics", "Udemy - Creative Photography"],
        "Personal Development": ["Coursera - Learning How to Learn", "Udemy - Time Management"]
    }
    result = resources.get(category, ["No resources available for this category"])
    return jsonify({"resources": result})

@app.route("/schedule-plan", methods=["POST"])
def schedule_plan():
    """
    This route returns a sample 4-day schedule plan.
    """
    schedule = [
        {"day": "Day 1", "activities": "Introduction and basics"},
        {"day": "Day 2", "activities": "Intermediate topics"},
        {"day": "Day 3", "activities": "Advanced concepts"},
        {"day": "Day 4", "activities": "Project work and review"}
    ]
    return jsonify({"schedule": schedule})

@app.route("/page")
def serve_page():
    """
    Serves the static index.html file if you want to display a page.
    """
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {"Content-Type": "text/html"}
    except Exception as e:
        return f"Error reading index.html: {e}", 500

# -------------------------------
# LOCAL TESTING (OPTIONAL)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
