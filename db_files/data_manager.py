import json
import os
import copy # Deep copy for data repair. Used for merging defaults.

DATADB_FILE = "db_files/data.json" # Main directory for user data file

# Default structure for every user account
DEFAULT_USER_DATA = {
    "tasks": [],
    "goals": [],
    "habits": [],
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

def merge_defaults(existing, defaults):
    """
    This function was added after I discovered a critical issue in the user data.
    I realized that nested data structures such as aim_trainer could not be repaired automatically.
    Since aim_trainer is a dictionary itself, that means it existed as a dictionary within a dictionary

    This function compares a user's existing data with the default data structure and automatically adds any missing fields.
    It loops through every key in the default structure. For each key, it performs one of two actions: check missing fields or nested dictionaries.
    If both values are dictionaries, then the function calls itself again. This is called recursion.
    The existing value will be preserved while the missing fields are restored.

    My old data manager system only checked the first level of the dictionary. 
    This meant that if fields inside aim_trainer are missing, then the system could never restore them.
    This function fixes that.
    """
    # Merge defaults into existing data, recursively for nested dictionaries
    if not isinstance(existing, dict) or not isinstance(defaults, dict):
        # If either is not a dictionary, do nothing
        return
    
    for key, value in defaults.items():
        # Missing field
        if key not in existing:
            # Using deepcopy, the original value is preserved. Only missing fields are added.
            existing[key] = copy.deepcopy(value)

        # Nested dictionary
        elif isinstance(value, dict) and isinstance(existing[key], dict):
            merge_defaults(existing[key], value) # Recursion

def get_user_data(username):
    # Load all data and return the specific user's data and auto-repair missing fields
    data = load_data()

    # Create account if it doesn't exist
    if username not in data:
        data[username] = copy.deepcopy(DEFAULT_USER_DATA)
        save_data(data)

    # Repair missing fields. Store before repair for comparison
    before = json.dumps(data[username], sort_keys=True)
    merge_defaults(data[username], DEFAULT_USER_DATA)
    after = json.dumps(data[username], sort_keys=True)

    # Save only if changes were made
    if before != after:
        save_data(data)

    return data[username]

def update_user_data(username, user_data):
    # Load all data, update the specific user's data, and save it back to the file
    data = load_data()
    data[username] = user_data
    save_data(data)