import os
import json
from flask import Flask, render_template, request, jsonify
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

SYSTEM_PROMPT = """You are an expert excuse generator. The user will describe a situation where they promised to do something but didn't follow through.

Generate exactly 3 excuses, ranked from most to least believable. For each excuse:
- Write 1-2 sentences
- Give a reliability score from 1-10
- Briefly explain (one phrase) why it's believable or not

Format your response as JSON only, no extra text:
[
  {"rank": 1, "excuse": "...", "reliability": 9, "why": "..."},
  {"rank": 2, "excuse": "...", "reliability": 6, "why": "..."},
  {"rank": 3, "excuse": "...", "reliability": 3, "why": "..."}
]

Rules:
- Excuses should feel realistic, not absurd
- Tailor them to the specific situation described
- Never repeat the same excuse type across the 3 options"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    situation = request.json.get("situation", "").strip()
    if not situation:
        return jsonify({"error": "Please describe your situation."}), 400

    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": situation}],
    )

    raw = message.content[0].text
    excuses = json.loads(raw)
    return jsonify({"excuses": excuses})


if __name__ == "__main__":
    app.run(debug=True)
