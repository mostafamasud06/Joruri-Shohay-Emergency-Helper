"""
knowledge_base.py
------------------
All the "facts" the agent relies on live here, in plain Python data
structures, so you (a beginner) can review, correct, and extend them
without touching any agent logic.

*** IMPORTANT BEFORE YOU SUBMIT ***
The hospital coordinates below are APPROXIMATE (based on general area
knowledge), not verified GPS pins. Before your demo/submission:
    1. Look up each hospital on Google Maps.
    2. Copy the exact latitude/longitude shown there.
    3. Replace the values below.
    This matters more here than in almost any other kind of project, because
    wrong location data in an emergency tool could genuinely mislead someone.
"""

if True:
    # ---------------------------------------------------------------------------
    # REAL, VERIFIED emergency numbers (Bangladesh) — do not change these unless
    # you re-verify them yourself; a wrong number here defeats the whole purpose.
    # ---------------------------------------------------------------------------
    EMERGENCY_NUMBERS = {
        "general": {
            "number": "999",
            "label_bn": "জাতীয় জরুরি সেবা (পুলিশ, ফায়ার সার্ভিস, অ্যাম্বুলেন্স)",
            "label_en": "National Emergency Service (Police, Fire, Ambulance) — 24/7, toll-free",
        },
        "disaster": {
            "number": "1090",
            "label_bn": "জাতীয় দুর্যোগ হটলাইন",
            "label_en": "National Disaster Management Hotline",
        },
        "women_child": {
            "number": "109",
            "label_bn": "নারী ও শিশু নির্যাতন প্রতিরোধ হেল্পলাইন",
            "label_en": "Women & Child Safety Helpline",
        },
    }

    # ---------------------------------------------------------------------------
    # Hospitals — starter set for Dhaka. Extend this list city by city.
    # tier: "free" (govt, effectively free/very low cost) | "low" | "mid" | "high"
    # specialty: list of tags used to match against the user's stated emergency
    # ---------------------------------------------------------------------------
    HOSPITALS = [
        {
            "name": "Dhaka Medical College Hospital (DMCH)",
            "area": "Bakshibazar, Dhaka",
            "lat": 23.7269,
            "lon": 90.3969,
            "tier": "free",
            "specialty": ["general", "trauma", "emergency"],
            "phone": "+880-2-55165088",
        },
        {
            "name": "National Institute of Traumatology & Orthopaedic Rehabilitation (NITOR)",
            "area": "Sher-e-Bangla Nagar, Dhaka",
            "lat": 23.7676,
            "lon": 90.3742,
            "tier": "free",
            "specialty": ["trauma", "fracture", "orthopedic"],
            "phone": "+880-2-55007337",
        },
        {
            "name": "National Institute of Burn & Plastic Surgery",
            "area": "near Dhaka Medical College, Dhaka",
            "lat": 23.7280,
            "lon": 90.3975,
            "tier": "free",
            "specialty": ["burn"],
            "phone": "+880-2-9660575",
        },
        {
            "name": "National Institute of Cardiovascular Diseases (NICVD)",
            "area": "Sher-e-Bangla Nagar, Dhaka",
            "lat": 23.7676,
            "lon": 90.3742,
            "tier": "free",
            "specialty": ["cardiac", "chest pain"],
            "phone": "+880-2-9126441",
        },
        {
            "name": "Kurmitola General Hospital",
            "area": "Airport Road, Dhaka",
            "lat": 23.8461,
            "lon": 90.3971,
            "tier": "free",
            "specialty": ["general", "emergency"],
            "phone": "+880-2-8991411",
        },
        {
            "name": "Ad-Din Women's Medical College Hospital",
            "area": "Moghbazar, Dhaka",
            "lat": 23.7461,
            "lon": 90.4062,
            "tier": "low",
            "specialty": ["maternity", "general"],
            "phone": "+880-2-9358972",
        },
        {
            "name": "Popular Diagnostic Centre & Hospital",
            "area": "Dhanmondi, Dhaka",
            "lat": 23.7461,
            "lon": 90.3742,
            "tier": "mid",
            "specialty": ["general", "diagnostic"],
            "phone": "+880-2-9661064",
        },
        {
            "name": "LabAid Hospital",
            "area": "Dhanmondi, Dhaka",
            "lat": 23.7465,
            "lon": 90.3760,
            "tier": "high",
            "specialty": ["general", "cardiac", "emergency"],
            "phone": "+880-2-9676356",
        },
        {
            "name": "Square Hospital",
            "area": "Panthapath, Dhaka",
            "lat": 23.7516,
            "lon": 90.3876,
            "tier": "high",
            "specialty": ["general", "trauma", "emergency", "cardiac"],
            "phone": "+880-2-8159457",
        },
        {
            "name": "United Hospital",
            "area": "Gulshan, Dhaka",
            "lat": 23.7929,
            "lon": 90.4152,
            "tier": "high",
            "specialty": ["general", "trauma", "emergency", "cardiac"],
            "phone": "+880-2-8836000",
        },
    ]

    # ---------------------------------------------------------------------------
    # First-aid guidance — kept deliberately generic and standard (the kind of
    # advice printed on Red Crescent / first-aid course cards). NOT medical
    # diagnosis. Always paired with "call 999" in the agent's actual replies.
    # ---------------------------------------------------------------------------
    # ---------------------------------------------------------------------------
    # Blood banks — starter set for Dhaka. IMPORTANT: we do NOT track live blood
    # stock anywhere (no real API for that exists that we can verify), so the
    # agent should always tell users to CALL and confirm current availability
    # themselves — never claim a blood type is "in stock" from this data.
    # *** VERIFY phone numbers before submission — marked where uncertain. ***
    # ---------------------------------------------------------------------------
    BLOOD_BANKS = [
        {
            "name": "Bangladesh Red Crescent Society Blood Center",
            "area": "Mohakhali, Dhaka",
            "lat": 23.7783,
            "lon": 90.4066,
            "phone": "VERIFY",  # look up current number before demo
            "note_bn": "জাতীয় রক্তদান সংস্থা, নিয়মিত রক্তদান কর্মসূচি পরিচালনা করে।",
            "note_en": "National blood donation organization with regular donation drives.",
        },
        {
            "name": "Sandhani (Dhaka Medical College Chapter)",
            "area": "Dhaka Medical College, Bakshibazar, Dhaka",
            "lat": 23.7269,
            "lon": 90.3969,
            "phone": "VERIFY",
            "note_bn": "স্বেচ্ছাসেবী রক্তদান সংগঠন, মেডিকেল শিক্ষার্থী পরিচালিত।",
            "note_en": "Volunteer blood donation organization, run by medical students.",
        },
        {
            "name": "Badhan (Dhaka University Chapter)",
            "area": "Dhaka University area, Dhaka",
            "lat": 23.7343,
            "lon": 90.3938,
            "phone": "VERIFY",
            "note_bn": "স্বেচ্ছাসেবী রক্তদাতা সংগঠন, বিশ্ববিদ্যালয়ভিত্তিক।",
            "note_en": "Volunteer blood donor organization, university-based network.",
        },
        {
            "name": "Quantum Foundation Blood Bank",
            "area": "Dhanmondi, Dhaka",
            "lat": 23.7461,
            "lon": 90.3742,
            "phone": "VERIFY",
            "note_bn": "স্থায়ী রক্তব্যাংক, রক্ত সংগ্রহ ও সরবরাহ করে।",
            "note_en": "Permanent blood bank facility, collects and supplies blood.",
        },
    ]

    FIRST_AID = {
        "bleeding": {
            "bn": [
                "পরিষ্কার কাপড় দিয়ে ক্ষতস্থানে সরাসরি চাপ দিন।",
                "রক্তক্ষরণ বন্ধ না হওয়া পর্যন্ত চাপ ধরে রাখুন।",
                "সম্ভব হলে আহত অংশ হৃদয়ের চেয়ে উঁচুতে রাখুন।",
                "অবিলম্বে ৯৯৯ এ কল করুন।",
            ],
            "en": [
                "Apply firm, direct pressure on the wound with a clean cloth.",
                "Keep the pressure on continuously until bleeding slows.",
                "If possible, raise the injured area above heart level.",
                "Call 999 immediately.",
            ],
        },
        "burn": {
            "bn": [
                "পোড়া স্থানে ঠান্ডা (বরফ নয়) পানি ঢালুন, কমপক্ষে ১০ মিনিট।",
                "ফোসকা ফাটাবেন না।",
                "পোড়া স্থানে মাখন/টুথপেস্ট লাগাবেন না — এটি ক্ষতি বাড়ায়।",
                "গুরুতর/বড় পোড়ার জন্য অবিলম্বে ৯৯৯ এ কল করুন।",
            ],
            "en": [
                "Run cool (not ice-cold) water over the burn for at least 10 minutes.",
                "Do not pop any blisters.",
                "Do not apply butter, toothpaste, or oil — these worsen burns.",
                "For serious or large burns, call 999 immediately.",
            ],
        },
        "choking": {
            "bn": [
                "ব্যক্তিকে সামনে ঝুঁকতে বলুন এবং পিঠে ৫ বার জোরে চাপড় দিন।",
                "কাজ না হলে হেইমলিখ ম্যানুভার (পেটে চাপ) প্রয়োগ করুন যদি প্রশিক্ষিত হন।",
                "শ্বাসনালী পরিষ্কার না হলে সাথে সাথে ৯৯৯ এ কল করুন।",
            ],
            "en": [
                "Lean the person forward and give 5 firm back blows between the shoulder blades.",
                "If that doesn't work and you're trained, perform abdominal thrusts (Heimlich maneuver).",
                "If the airway isn't clear, call 999 immediately.",
            ],
        },
        "unconscious": {
            "bn": [
                "ব্যক্তি শ্বাস নিচ্ছে কিনা পরীক্ষা করুন।",
                "শ্বাস নিলে, তাকে পাশ ফিরিয়ে শোয়ান (recovery position)।",
                "শ্বাস না নিলে এবং আপনি প্রশিক্ষিত হলে CPR শুরু করুন।",
                "অবিলম্বে ৯৯৯ এ কল করুন — সময় নষ্ট করবেন না।",
            ],
            "en": [
                "Check if the person is breathing.",
                "If breathing, turn them onto their side (recovery position).",
                "If not breathing and you're trained, begin CPR.",
                "Call 999 immediately — do not delay this step.",
            ],
        },
        "fracture": {
            "bn": [
                "আহত অংশ নাড়াবেন না বা সোজা করার চেষ্টা করবেন না।",
                "সম্ভব হলে শক্ত কিছু দিয়ে (splint) অংশটি স্থির রাখুন।",
                "ব্যক্তিকে যতটা সম্ভব স্থির রাখুন এবং সাহায্যের জন্য ৯৯৯ এ কল করুন।",
            ],
            "en": [
                "Do not move or try to straighten the injured limb.",
                "If possible, immobilize it with a splint (any firm, straight object).",
                "Keep the person as still as possible and call 999 for help.",
            ],
        },
        "earthquake": {
            "bn": [
                "ড্রপ, কভার, হোল্ড অন: মেঝেতে বসুন, শক্ত টেবিলের নিচে যান, ধরে রাখুন।",
                "জানালা, কাচ ও ভারী আসবাবপত্র থেকে দূরে থাকুন।",
                "ভূমিকম্প থামার পর, ভবন থেকে বের হয়ে খোলা জায়গায় যান।",
                "আফটারশক হতে পারে — সতর্ক থাকুন।",
                "সর্বশেষ তথ্য ও দুর্যোগ সহায়তার জন্য ১০৯০ নম্বরে কল করুন।",
            ],
            "en": [
                "Drop, Cover, and Hold On: get low, take cover under a sturdy table, and hold on.",
                "Stay away from windows, glass, and heavy furniture that could fall.",
                "Once shaking stops, move to open ground away from damaged buildings.",
                "Aftershocks are common — stay alert.",
                "Call 1090 (national disaster hotline) for official updates and help.",
            ],
        },
    }
