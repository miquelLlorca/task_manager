from datetime import datetime
import json
import os

EVENT_FILE = "data/events.json"
CATEGORY_FILE = "data/categories.json"


def load_events():
    if os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, "r") as f:
            return json.load(f)
    return []

def save_events(events):
    with open(EVENT_FILE, "w") as f:
        json.dump(events, f, indent=2)


def load_categories():
    if os.path.exists(CATEGORY_FILE):
        with open(CATEGORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_categories(categories):
    with open(CATEGORY_FILE, "w") as f:
        json.dump(categories, f, indent=2)







def get_color_from_category(categories, category_name):
    for c in categories:
        if(c['name']==category_name):
            return c['color']


def to_date_str(iso_like):
    """Return 'YYYY-MM-DD' from an ISO-like datetime string or date string."""
    if iso_like is None:
        return None
    # if it's already a date object
    if isinstance(iso_like, datetime):
        return iso_like.date().isoformat()
    s = str(iso_like)
    # prefer startStr if provided like '2025-01-20'
    if "T" in s:
        return s.split("T")[0]
    return s  # assume it's already 'YYYY-MM-DD'