import json
import os

DATADB_FILE = "db_files/data.json"

def load_data():
    if not os.path.exists(DATADB_FILE):
        return {}

    with open(DATADB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATADB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_user_data(username):
    data = load_data()

    if username not in data:
        data[username] = {
            "tasks": [],
            "goals": []
        }
        save_data(data)

    return data[username]

def update_user_data(username, user_data):
    data = load_data()
    data[username] = user_data
    save_data(data)