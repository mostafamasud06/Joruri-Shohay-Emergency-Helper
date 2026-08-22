
"""
tools.py
--------
Three tools. Each one is a plain Python function the agent can call when it
decides it's relevant — the docstring is what teaches the agent WHEN to use it.
"""

import math
import json
import requests
from datetime import datetime, timezone
from pathlib import Path
from strands import tool
from knowledge_base import EMERGENCY_NUMBERS, HOSPITALS, FIRST_AID, BLOOD_BANKS


def _haversine_km(lat1, lon1, lat2, lon2):
    """Straight-line distance between two GPS points, in kilometers.
    Not real road distance, but good enough to rank 'closest' options
    for a hackathon demo. A real product would use a maps/routing API."""
    R = 6371  # Earth's radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


@tool
def geocode_location(place_name: str) -> str:
    """Convert a place name or area (e.g. "Dhanmondi, Dhaka", "Mirpur 10")
    into real latitude/longitude coordinates, using OpenStreetMap's free
    Nominatim geocoding service. Use this whenever the user mentions an
    area by name instead of giving coordinates directly — call this FIRST,
    then pass the resulting lat/lon into find_hospitals or find_blood_banks.

    Args:
        place_name: The place or area name, ideally with city/country for
        accuracy, e.g. "Dhanmondi, Dhaka, Bangladesh".

        Returns:
            "lat,lon" as plain text if found, or "NOT_FOUND" if the place
            couldn't be geocoded — in that case, ask the user for a nearby
            well-known landmark instead of guessing coordinates yourself.
            """
    try:
                # Always bias toward Bangladesh unless the user already specified
                # a country, since that's this agent's primary service area.
                query = place_name if "bangladesh" in place_name.lower() else f"{place_name}, Bangladesh"

                response = requests.get(
                    "https://nominatim.openstreetmap.org/search",
                    params={"q": query, "format": "json", "limit": 1},
                    headers={"User-Agent": "JoruriShohay-Hackathon-Agent/1.0"},  # required by Nominatim's usage policy
                    timeout=8,
                )
                response.raise_for_status()
                results = response.json()
                if not results:
                    return "NOT_FOUND"
                lat, lon = results[0]["lat"], results[0]["lon"]
                return f"{lat},{lon}"
    except Exception as e:
                return f"NOT_FOUND (error: {e})"


@tool
def find_hospitals(user_lat: float, user_lon: float, emergency_type: str, budget: str) -> str:
    """Find the closest suitable hospitals for a medical emergency, filtered
    by the type of emergency and the user's budget tier.

    Args:
        user_lat: User's current latitude (ask the user for their area if
        they don't know exact coordinates, and estimate from a
        known Dhaka landmark near them).
        user_lon: User's current longitude.
        emergency_type: One of: general, trauma, fracture, burn, cardiac,
        maternity, diagnostic, emergency.
        budget: One of: "free" (can't pay), "low" (very limited funds),
        "mid" (can pay a moderate private bill), "high" (can afford
        premium private care). If the user is unsure, use "low".

        Returns:
            A ranked list (closest first) of up to 3 matching hospitals with
            name, area, phone, and approximate distance in km.
            """
    tier_order = {
        "free": ["free", "low", "mid", "high"],
        "low": ["free", "low", "mid", "high"],
        "mid": ["mid", "low", "free", "high"],
        "high": ["high", "mid", "low", "free"],
    }
    allowed_tiers = tier_order.get(budget, tier_order["low"])
    candidates = [
        h for h in HOSPITALS
        if emergency_type.lower() in h["specialty"] and h["tier"] in allowed_tiers
    ]
    if not candidates:
        candidates = [h for h in HOSPITALS if h["tier"] in allowed_tiers]
    if not candidates:
        return "NO_MATCH_FOUND"

    ranked = sorted(
        candidates,
        key=lambda h: _haversine_km(user_lat, user_lon, h["lat"], h["lon"]),
    )
    lines = []
    for h in ranked[:3]:
        dist = round(_haversine_km(user_lat, user_lon, h["lat"], h["lon"]), 1)
        lines.append(
            f"- {h['name']} ({h['area']}) — approx {dist} km away, "
            f"tier: {h['tier']}, phone: {h['phone']}"
        )
    return "\n".join(lines)


@tool
def get_emergency_number(need: str) -> str:
    """Get the correct real emergency phone number to call right now.

    Args:
        need: One of "general" (any accident/crime/fire/ambulance need),
        "disaster" (earthquake, flood, major disaster), or
        "women_child" (women/child safety concerns).

        Returns:
            The phone number and what it's for, in Bangla and English.
            """
    entry = EMERGENCY_NUMBERS.get(need, EMERGENCY_NUMBERS["general"])
    return f"{entry['number']} — {entry['label_bn']} / {entry['label_en']}"


@tool
def find_blood_banks(user_lat: float, user_lon: float, blood_type: str = "") -> str:
    """Find nearby blood banks/donation organizations when someone needs
    blood urgently (e.g. surgery, accident, thalassemia patients, childbirth
    complications).

    IMPORTANT: This does NOT show live blood stock — that data isn't
    reliably available. Always tell the user to call and confirm current
    availability of their specific blood type themselves.

    Args:
        user_lat: User's current latitude.
        user_lon: User's current longitude.
        blood_type: The blood type needed (e.g. "O+", "AB-"), if known.
        Can be empty if unknown.

        Returns:
            A ranked list (closest first) of blood banks with name, area, and
            phone — plus a reminder to call and confirm stock directly.
            """
    if not BLOOD_BANKS:
        return "NO_MATCH_FOUND"

    ranked = sorted(
        BLOOD_BANKS,
        key=lambda b: _haversine_km(user_lat, user_lon, b["lat"], b["lon"]),
    )

    lines = []
    for b in ranked[:3]:
        dist = round(_haversine_km(user_lat, user_lon, b["lat"], b["lon"]), 1)
        lines.append(f"- {b['name']} ({b['area']}) — approx {dist} km away, phone: {b['phone']}")

    type_note = f" for blood type {blood_type}" if blood_type else ""
    lines.append(
        f"\nCall ahead{type_note} to confirm current stock before traveling — "
        "availability changes hour to hour and isn't tracked here live."
    )
    return "\n".join(lines)


FEEDBACK_LOG_PATH = Path(__file__).parent / "feedback_log.jsonl"


@tool
def submit_user_feedback(category: str, details: str) -> str:
    """Log a correction or piece of real-world information a user offers —
    e.g. an actual cost they paid, a wrong phone number, a hospital that's
    closed, or a suggestion for the service. This does NOT change the
    agent's knowledge immediately (that would risk unverified data being
    trusted) — it saves the info for a human to review and add later.

    Use this whenever a user says something like "actually it costs X",
    "that number doesn't work", "you should add Y hospital", etc.

    Args:
        category: Short label, e.g. "cost_update", "wrong_number",
        "new_hospital", "general_suggestion".
        details: The actual information or suggestion the user provided.

        Returns:
            A confirmation message to show the user.
            """
    entry = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "category": category,
                "details": details,
            }
    try:
        with open(FEEDBACK_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return "Thank you — I've logged this for review. It'll be checked before being added to the official information."
    except Exception as e:
        return f"Couldn't save feedback right now ({e}), but thank you for sharing it."


@tool
def first_aid_steps(situation: str) -> str:
    """Get basic, standard first-aid steps for a specific situation while
    waiting for professional help to arrive. This is general safety guidance
    only, never a diagnosis or a substitute for medical care — always pair
    this with telling the user to call 999.

    Args:
        situation: A short description or keyword for what's wrong — e.g.
        "bleeding", "heavy bleeding", "burn", "choking",
        "unconscious", "fracture", "broken arm", "earthquake".
        Natural phrases are fine; this matches flexibly.

        Returns:
            Numbered first-aid steps in Bangla and English, or a message if the
            situation isn't covered.
            """
    situation_lower = situation.lower()

    # Try an exact key match first (fast path).
    entry = FIRST_AID.get(situation_lower)

    # Fall back to flexible keyword matching so phrasings like "heavy
    # bleeding", "broken arm", or "passed out" still map correctly, instead
    # of silently failing and pushing Claude to invent its own advice.
    if not entry:
        keyword_map = {
            "bleeding": ["bleed", "blood loss", "রক্তক্ষরণ", "রক্ত পড়"],
            "burn": ["burn", "scald", "পোড়া"],
            "choking": ["chok", "airway", "swallowed", "শ্বাসনালী", "গলায়"],
            "unconscious": ["uncon", "faint", "passed out", "not breathing", "অজ্ঞান", "শ্বাস নিচ্ছে না"],
            "fracture": ["fracture", "broken", "bone", "sprain", "ভাঙা", "হাড়"],
            "earthquake": ["earthquake", "quake", "shaking", "ভূমিকম্প"],
        }
        for category, keywords in keyword_map.items():
            if any(kw in situation_lower for kw in keywords):
                entry = FIRST_AID.get(category)
                break

    if not entry:
        return "NOT_COVERED — advise the user to call 999 and describe the situation to the operator. Do not invent first-aid steps yourself."

    bn_steps = "\n".join(f"{i+1}. {s}" for i, s in enumerate(entry["bn"]))
    en_steps = "\n".join(f"{i+1}. {s}" for i, s in enumerate(entry["en"]))
    return f"বাংলা:\n{bn_steps}\n\nEnglish:\n{en_steps}"

