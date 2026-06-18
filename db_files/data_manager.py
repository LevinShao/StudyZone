import json
import os

DATADB_FILE = "db_files/data.json" # Main directory for user data file

def load_data():
    # If the data file doesn't exist, return an empty dictionary
    if not os.path.exists(DATADB_FILE):
        return {}

    with open(DATADB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    # Save the provided data dictionary to the JSON file with indentation for readability
    with open(DATADB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_data(username):
    # Load all data and return the specific user's data
    data = load_data()

    if username not in data:
        data[username] = {
            "tasks": [],
            "goals": [],
            "habits": [],
            "notebook": [],
            "events": [],
            "flashcards": [],
            "sticky_notes": [],
            "journal_entries": [],
            "aim_trainer": {
                "high_score": 0,
                "games_played": 0,
                "best_accuracy": 0
            },
            "reaction_trainer": {
                "best_time": 0
            }
        }
        save_data(data)

    # Ensure older accounts get missing fields
    defaults = {
        "tasks": [],
        "goals": [],
        "habits": [],
        "notebook": [],
        "events": [],
        "flashcards": [],
        "sticky_notes": [],
        "journal_entries": [],
        "aim_trainer": {
            "high_score": 0,
            "games_played": 0,
            "best_accuracy": 0
        },
        "reaction_trainer": {
            "best_time": 0
        }
    }

    changed = False

    for key, value in defaults.items():
        if key not in data[username]:
            data[username][key] = value
            changed = True

    if changed:
        save_data(data)

    return data[username]

def update_user_data(username, user_data):
    # Load all data, update the specific user's data, and save it back to the file
    data = load_data()
    data[username] = user_data
    save_data(data)