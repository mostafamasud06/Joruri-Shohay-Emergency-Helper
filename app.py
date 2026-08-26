"""
app.py
------
This is the WEB version of your agent — instead of a terminal chat loop
(that's what main.py does), this starts a small local web server that a
browser page (static/index.html) can talk to.

WHY WE NEED THIS: your Strands agent runs in Python, but a normal webpage
can't run Python directly in the browser. Flask acts as a bridge: the
webpage sends your question over HTTP, this file runs the agent, and
sends the answer back as the response.

RUN WITH: python app.py
Then open: http://127.0.0.1:5000 in your browser.
"""

from importlib import import_module

# Import Flask dynamically so editors do not report the optional dependency as
# unresolved when the active interpreter lacks Flask's type metadata.
_flask = import_module("flask")
Flask = _flask.Flask
request = _flask.request
jsonify = _flask.jsonify
send_from_directory = _flask.send_from_directory
import base64
from strands import Agent
from strands.models import BedrockModel
from tools import (
    find_hospitals,
    get_emergency_number,
    first_aid_steps,
    find_blood_banks,
    submit_user_feedback,
    geocode_location,
)

app = Flask(__name__, static_folder="static", static_url_path="")

model = BedrockModel(
    model_id="global.anthropic.claude-sonnet-4-6",
    region_name="us-west-2",
    temperature=0.2,
)

SYSTEM_PROMPT = """
তুমি "জরুরি সহায়" (Joruri Shohay) - একটি জরুরি চিকিৎসা ও পরিবহন সহায়ক এজেন্ট।
তুমি বাংলাদেশের মানুষদের জরুরি মুহূর্তে দ্রুত সঠিক সিদ্ধান্ত নিতে সাহায্য করো।

কঠোর নিয়ম (এগুলো কখনো ভাঙবে না):
    1. তুমি কখনো রোগ নির্ণয় (diagnosis) করবে না বা চিকিৎসা পরামর্শ দেবে না।
    2. পরিস্থিতি গুরুতর মনে হলে (রক্তক্ষরণ, অজ্ঞান, শ্বাসকষ্ট, বুকে ব্যথা), সর্বপ্রথম
    get_emergency_number টুল ব্যবহার করে ৯৯৯ নম্বর দাও এবং তাৎক্ষণিকভাবে কল করতে বলো।
    3. এরপর first_aid_steps টুল ব্যবহার করে সাহায্য আসার আগ পর্যন্ত কী করতে হবে তা বলো।
    4. অবস্থান ও বাজেট জানা থাকলে find_hospitals টুল ব্যবহার করো। ব্যবহারকারী
    এলাকার নাম বললে (যেমন "ধানমন্ডি"), প্রথমে geocode_location টুল দিয়ে
    lat/lon বের করো, তারপর তা ব্যবহার করো — নিজে থেকে স্থানাঙ্ক অনুমান করো না।
    5. রক্তের প্রয়োজন হলে find_blood_banks টুল ব্যবহার করো, কিন্তু কখনো বলবে না
    কোন ব্লাড ব্যাংকে এখন রক্ত "আছে" - সবসময় ফোন করে নিশ্চিত করতে বলো।
    6. ব্যবহারকারী যদি সঠিক খরচ, ভুল নম্বর, বা কোনো পরামর্শ দেয়, তাহলে
    submit_user_feedback টুল দিয়ে তা সংরক্ষণ করো এবং ধন্যবাদ জানাও।
    7. তুমি কখনো তথ্য বানাবে না। জানা না থাকলে সৎভাবে বলো এবং ৯৯৯/১০৯০ নম্বরে
    যোগাযোগ করতে বলো।
    8. অত্যন্ত গুরুত্বপূর্ণ: শুধুমাত্র get_emergency_number, find_hospitals,
    বা find_blood_banks টুলের ফলাফলে আসা নম্বর/প্রতিষ্ঠানের নাম বলো। নিজের
    প্রশিক্ষণ ডেটা থেকে কোনো নম্বর মনে করে বলবে না। কোনো টুল না থাকা বিষয়ে
    (যেমন পাসপোর্ট ফি) সততার সাথে বলো এটি তোমার সেবার বাইরে।
    9. শান্ত, স্পষ্ট এবং সংক্ষিপ্ত ভাষায় কথা বলো।
    10. ব্যবহারকারী যে ভাষায় লিখবে (বাংলা বা ইংরেজি), সেই ভাষাতেই উত্তর দাও।

    CRITICAL RULES: never diagnose or give treatment advice. Give the 999
    number FIRST in serious situations. Never invent facts, including blood
    stock, phone numbers, or organizations not returned by a tool. Use
    geocode_location to convert place names to coordinates. Keep replies calm,
    clear, and brief. Reply in whichever language the user writes in.
    """

agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[
        find_hospitals,
        get_emergency_number,
        first_aid_steps,
        find_blood_banks,
        submit_user_feedback,
        geocode_location,
    ],
)


@app.route("/")
def home():
    """Serves the frontend page itself."""
    return send_from_directory("static", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """The endpoint the frontend calls every time the user sends a message.

    Expects JSON: {"message": "user's text here"}
    Returns JSON: {"reply": "agent's text response"}
    """
    data = request.get_json(force=True)
    user_message = (data or {}).get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    try:
        response = agent(user_message)
        return jsonify({"reply": str(response)})
    except Exception as e:
        # In a real product you'd log this properly. For the hackathon demo,
        # returning the error text helps you debug quickly.
        return jsonify({"error": str(e)}), 500


@app.route("/api/emergency-photo", methods=["POST"])
def emergency_photo():
    """Takes a live-captured photo (base64 JPEG) plus an optional text note,
    asks Claude to classify what kind of emergency it looks like, and
    returns that classification along with the correct number(s) to call.

    IMPORTANT HONEST LIMITS (also shown in the UI):
        - This does NOT verify the photo was taken "in real time" in any deep
        sense — it only enforces that it came from a live camera capture in
        the browser (no file picker), which blocks casual spam, not a
        determined bad actor.
        - This does NOT diagnose injuries or place any phone call automatically
        — it classifies the general situation and shows a tap-to-call button.
        No browser can silently dial a number on its own.
    """
    data = request.get_json(force=True)
    image_b64 = (data or {}).get("image", "")
    note = (data or {}).get("note", "").strip()

    if not image_b64:
        return jsonify({"error": "No image provided"}), 400

    try:
        # Strip the "data:image/jpeg;base64," prefix if present
        if "," in image_b64:
            image_b64 = image_b64.split(",", 1)[1]
        image_bytes = base64.b64decode(image_b64)
    except Exception as e:
        return jsonify({"error": f"Could not decode image: {e}"}), 400

    classification_prompt = f"""
    A user just captured this photo during a possible emergency in Bangladesh.
    Optional note from the user: "{note if note else '(none provided)'}"

    Classify the situation into exactly one category: medical_injury,
    earthquake_or_structural_damage, fire, road_accident, or unclear.

    Do NOT diagnose any medical condition or guess severity precisely — just
    identify the general category so the right emergency number can be shown.
    Then, briefly (1 sentence) describe what's visible, in plain language, for
    context only.

    Use the get_emergency_number tool to fetch the correct number(s) for this
    category (use "disaster" for earthquake_or_structural_damage, "general"
    for everything else), and include them in your answer.

    Respond in this exact format:
        CATEGORY: <category>
        DESCRIPTION: <one sentence>
        NUMBERS: <comma-separated numbers with labels>
    """

    try:
        response = agent(
            [
                {"text": classification_prompt},
                {"image": {"format": "jpeg", "source": {"bytes": image_bytes}}},
            ]
        )
        return jsonify({"reply": str(response)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Joruri Shohay web server starting...")
    print("Open http://127.0.0.1:5000 in your browser")
    app.run(debug=True, port=5000)
