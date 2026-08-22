# জরুরি সহায় (Joruri Shohay) — Emergency Medical & Transport Helper

An AI agent built with [Strands Agents SDK](https://strandsagents.com) that helps
people in Bangladesh make fast, correct decisions in a medical emergency —
which real number to call, what to do while help arrives, and which nearby
hospital fits their budget.

**Problem:** In a medical emergency, minutes matter — but many people don't
know the right number to call, what basic first aid to do while waiting, or
which hospital they can actually afford and reach in time. This gets far
worse in disaster scenarios (e.g. the 2026 earthquakes that killed thousands
in Venezuela and Colombia) in a dense, high-risk country like Bangladesh.

**Who it's for:** Anyone in a medical emergency — from everyday accidents and
sudden illness to mass-casualty disaster scenarios — especially people
without a clear sense of the nearest affordable hospital.

**Why it matters:** Confusion costs time, and time costs lives. This agent
compresses "who do I call, what do I do, where do I go" into one fast,
calm answer.

---

## Design philosophy (read this before extending the project)

This is a **safety-critical** tool, so it's built with deliberate limits:

- It **never diagnoses** or gives treatment advice — only logistics
  (numbers, hospitals) and standard first-aid steps.
- It **always gives the real 999 number first** in serious situations,
  before anything else.
- It **does not invent data.** Where I don't have verified real-time
  information (e.g. live disaster shelter locations), the agent points to
  the real official hotline (1090) instead of guessing.
- Hospital data is a **small, illustrative starter set for Dhaka** —
  see the warning at the top of `knowledge_base.py` about verifying
  coordinates before your demo.

Keep this philosophy as you extend it — resist the urge to fabricate
data to make the demo look more complete. Judges (and worse, real users)
that catch a wrong hospital location or phone number will trust the whole
project less.

---

## Setup

```bash
cd joruri-shohay
python -m venv .venv
source .venv/Scripts/activate      # Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt

export AWS_PROFILE=bedrock
export AWS_REGION=us-west-2     # match your enabled Bedrock region

python app.py                   # runs the actual web product (recommended)
# python main.py                # alternative: terminal/CLI version, useful for quick debugging
```

`python app.py` starts a local web server — open **http://127.0.0.1:5000** in your browser to use it. This is the real submission entry point; `main.py` is kept only as a lightweight terminal version for quick testing.

Try asking:

- "আমার বাবার হঠাৎ বুকে ব্যথা হচ্ছে, আমি ধানমন্ডিতে আছি" (my father has sudden chest pain, I'm in Dhanmondi)
- "There's been a road accident, someone is bleeding badly, what do I do?"
- "ভূমিকম্প হচ্ছে, কী করব?" (there's an earthquake happening, what do I do?)
- "I need O-negative blood urgently, I'm near Dhanmondi"

---

## File structure

| File                 | What it does                                                                                                                            |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `knowledge_base.py`  | Emergency numbers, hospital database, blood banks, first-aid steps. **Edit this to add cities/hospitals.**                              |
| `tools.py`           | Six tools: `geocode_location`, `find_hospitals`, `find_blood_banks`, `get_emergency_number`, `first_aid_steps`, `submit_user_feedback`. |
| `main.py`            | Terminal/CLI version of the agent — useful for quick testing.                                                                           |
| `app.py`             | **The real product** — a Flask web server exposing the agent through `static/index.html`.                                               |
| `static/index.html`  | The actual frontend: chat UI with dark/light theme and Bangla/English language toggles.                                                 |
| `feedback_log.jsonl` | Auto-created once users submit corrections/suggestions — review and merge into `knowledge_base.py` manually. Not committed to git.      |

---

## Language note (important for judges)

The agent replies in whichever language the user writes in (Bangla or English) — this is intentional, since real users in Bangladesh are often more comfortable typing in Bangla. All submission materials (this README, code comments, the demo video) are in English to meet the hackathon's English-language requirement; the product's bilingual behavior is a deliberate accessibility feature for the target audience, not a submission-language issue.

---

## Before you submit — a verification checklist

- [ ] Confirm every hospital's exact coordinates on Google Maps (current values are approximate)
- [ ] Confirm every hospital's phone number is current
- [ ] Confirm 999 / 1090 / 109 are still correct (they should be stable, but verify)
- [ ] Test with a few real people describing real (past, resolved) emergencies and see if the response feels genuinely useful
- [ ] Make sure the agent NEVER skips telling the user to call 999 first in a serious scenario — test this explicitly with a few different phrasings

---

## Where to improve (priority order)

1. **Expand hospital coverage beyond Dhaka** — Chittagong, Sylhet, Khulna,
   etc. This is the highest-impact, lowest-complexity next step.
2. **Real routing distance, not straight-line** — integrate a maps/routing
   API (e.g. Google Maps Directions API, or OpenStreetMap's OSRM which is
   free) so "nearest" accounts for actual roads, not straight-line distance.
3. **WhatsApp interface** — nobody in a real emergency will open a terminal.
   This is the single most important thing for genuine impact.
4. **Amazon Bedrock AgentCore deployment** — turns this into an always-on
   hosted agent, and strengthens your Technical Implementation score per
   the hackathon rules.
5. **Ambulance dispatch integration** — if any local ambulance service
   (Red Crescent, Fire Service) exposes a bookable number or API, surface
   it directly rather than just displaying the general 999 line.
6. **Offline fallback** — a lightweight SMS-based version for when data
   connectivity is the actual bottleneck (common in disaster scenarios).
7. **Multi-language beyond Bangla/English** — consider Chittagonian or
   other regional dialects if you have capacity.

---

## License

MIT — see `LICENSE`.
