import os
from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

# -------------------------------
# FLASK APP SETUP
# -------------------------------
app = Flask(__name__)
CORS(app)  # Enable CORS to handle cross-origin requests

# Configuration: use environment variable for OpenAI API key
app.config["SECRET_KEY"] = "1234"
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    print("WARNING: OPENAI_API_KEY environment variable is not set!")

# -------------------------------
# FLASK ROUTES
# -------------------------------

@app.route("/")
def index():
    # Simple route to test server status
    return "Hello from Flask! This is your Roadmap Planner Chatbot."

@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    """
    Expects JSON: { "prompt": "your prompt" }
    Returns JSON: { "roadmap": "generated text" }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"roadmap": "Error: No valid JSON provided."}), 400

    prompt = data.get("prompt", "")
    try:
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
    Expects JSON: { "category": "Technology" }
    Returns JSON: { "resources": [ ... ] }
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"resources": ["Error: No valid JSON provided."]}), 400

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
    Returns a sample 4-day schedule plan.
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
    Serves the static index.html file.
    """
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {"Content-Type": "text/html"}
    except Exception as e:
        return f"Error reading index.html: {e}", 500

# -------------------------------
# GLOBAL ERROR HANDLERS
# -------------------------------
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method Not Allowed. Please use POST."}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal Server Error"}), 500

# -------------------------------
# LOCAL TESTING (OPTIONAL)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
