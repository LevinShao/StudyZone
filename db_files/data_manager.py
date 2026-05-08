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
    # Load all data and return the specific user's data (right now, tasks and goals)
    data = load_data()

    if username not in data:
        data[username] = {
            "tasks": [],
            "goals": []
        }
        save_data(data)

    return data[username]

def update_user_data(username, user_data):
    # Load all data, update the specific user's data, and save it back to the file
    data = load_data()
    data[username] = user_data
    save_data(data)