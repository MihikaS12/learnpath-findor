import sys
from io import BytesIO
from flask import Flask, request, jsonify
import openai

# -------------------------------
# FLASK APP SETUP
# -------------------------------
app = Flask(__name__)

# Configuration (Customize as needed)
app.config["SECRET_KEY"] = "1234"
app.config["OPENAI_API_KEY"] = "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"  # Replace with actual key
openai.api_key = app.config["OPENAI_API_KEY"]

# -------------------------------
# FLASK ROUTES
# -------------------------------

# Example route to test if your server is running
@app.route("/")
def index():
    return "Hello from Flask (Custom Adapter)!"

# Route: Generate Plan
@app.route("/generate-plan", methods=["POST"])
def generate_plan():
    data = request.get_json()
    prompt = data.get('prompt', '')

    try:
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

# Route: Fetch Resources
@app.route("/fetch-resources", methods=["POST"])
def fetch_resources():
    data = request.get_json()
    category = data.get('category', '')

    resources = {
        "Technology": ["Coursera - Python for Everybody", "Udemy - Web Dev Bootcamp"],
        "Business": ["edX - Business Foundations", "LinkedIn Learning - Marketing Strategies"],
        "Creative Arts": ["Skillshare - Graphic Design Basics", "Udemy - Creative Photography"],
        "Personal Development": ["Coursera - Learning How to Learn", "Udemy - Time Management"]
    }

    result = resources.get(category, ["No resources available for this category"])
    return jsonify({"resources": result})

# Route: Schedule Plan
@app.route("/schedule-plan", methods=["POST"])
def schedule_plan():
    schedule = [
        {"day": "Day 1", "activities": "Introduction and basics"},
        {"day": "Day 2", "activities": "Intermediate topics"},
        {"day": "Day 3", "activities": "Advanced concepts"},
        {"day": "Day 4", "activities": "Project work and review"}
    ]
    return jsonify({"schedule": schedule})

# Optional route to serve index.html from disk (if you want to display a page)
@app.route("/page")
def serve_page():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return content, 200, {"Content-Type": "text/html"}

# -------------------------------
# CUSTOM HANDLER FOR VERCEL
# -------------------------------
def handler(vercel_request, context):
    """
    This function is the entry point for the Vercel serverless function.
    We manually convert the Vercel request into a WSGI environ dict,
    call the Flask app, and return a response in Vercel's format.
    """

    # 1) Build a WSGI environ dictionary from the Vercel request.
    environ = {
        "REQUEST_METHOD": vercel_request.method,
        "PATH_INFO": vercel_request.path or "/",
        "QUERY_STRING": vercel_request.query or "",
        "SERVER_NAME": "localhost",
        "SERVER_PORT": "80",
        "wsgi.version": (1, 0),
        "wsgi.input": BytesIO(vercel_request.body or b""),
        "wsgi.errors": sys.stderr,
        "wsgi.run_once": False,
        "wsgi.url_scheme": "http",
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
    }

    # 2) Capture the Flask response status and headers via start_response.
    response_status = []
    response_headers = []

    def start_response(status, headers, exc_info=None):
        response_status.append(status)
        response_headers.extend(headers)

    # 3) Call the Flask WSGI app.
    response_iter = app(environ, start_response)
    response_body = b"".join(response_iter)

    # 4) Parse the status code (e.g., "200 OK" -> 200).
    if response_status:
        status_code_str = response_status[0].split()[0]
        try:
            status_code = int(status_code_str)
        except ValueError:
            status_code = 500
    else:
        status_code = 500

    # Convert headers list to a dictionary
    headers_dict = {k: v for k, v in response_headers}

    # 5) Return the data in Vercel's expected format
    return {
        "statusCode": status_code,
        "headers": headers_dict,
        "body": response_body.decode("utf-8")
    }

# -------------------------------
# LOCAL TESTING (OPTIONAL)
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)