"""Static reference data for the Boundary Waters demo tools.

Kept as in-memory mock data (no external API calls) so the server is fully
self-contained and reliable for live demos.
"""

ENTRY_POINTS = {
    "EP16": {
        "name": "Moose Lake",
        "permit_quota_per_day": 20,
        "typical_portages": 0,
        "difficulty": "easy",
        "nearest_town": "Ely, MN",
    },
    "EP24": {
        "name": "Fall Lake",
        "permit_quota_per_day": 15,
        "typical_portages": 1,
        "difficulty": "easy",
        "nearest_town": "Ely, MN",
    },
    "EP30": {
        "name": "Lake One",
        "permit_quota_per_day": 15,
        "typical_portages": 3,
        "difficulty": "moderate",
        "nearest_town": "Ely, MN",
    },
    "EP38": {
        "name": "North Kawishiwi River",
        "permit_quota_per_day": 6,
        "typical_portages": 4,
        "difficulty": "moderate",
        "nearest_town": "Ely, MN",
    },
    "EP68": {
        "name": "Brule Lake",
        "permit_quota_per_day": 9,
        "typical_portages": 2,
        "difficulty": "moderate",
        "nearest_town": "Grand Marais, MN",
    },
}

CAMPSITES = {
    "Moose Lake": ["Moose Lake #3 (island)", "Moose Lake #7 (north shore)"],
    "Fall Lake": ["Fall Lake #2", "Fall Lake #5 (near narrows)"],
    "Lake One": ["Lake One #4", "Lake One #9 (point site)"],
    "Basswood Lake": ["Basswood #12 (Jackfish Bay)", "Basswood #19"],
    "Brule Lake": ["Brule #6", "Brule #14 (west arm)"],
}

FISHING_REGS = {
    "walleye": {"daily_limit": 6, "possession_limit": 6, "min_length_in": None},
    "northern_pike": {"daily_limit": 3, "possession_limit": 6, "min_length_in": None},
    "smallmouth_bass": {"daily_limit": 6, "possession_limit": 6, "min_length_in": None},
    "lake_trout": {"daily_limit": 3, "possession_limit": 3, "min_length_in": None},
}

GEAR_CHECKLIST = [
    "Canoe + paddles (spare paddle recommended)",
    "PFDs (one per person, worn while on water)",
    "Portage yoke / pack straps",
    "Duluth pack(s)",
    "Water filter or purification tablets",
    "Bear-proof food canister or rope for a bear hang",
    "Map + compass (BWCA permits require no motorized GPS-only nav)",
    "First aid kit",
    "Fire starter, stored dry",
    "Rain gear",
]
