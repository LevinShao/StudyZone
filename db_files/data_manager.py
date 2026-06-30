import json
import os
import shutil # For copying files (backup)

DATADB_FILE = "db_files/data.json" # Main directory for user data file
DATADB_BACKUP = "db_files/backup/data_backup.json" # Backup file for user data

ACCOUNTDB_FILE = "db_files/users.json" # Main directory for user account file
ACCOUNTDB_BACKUP = "db_files/backup/users_backup.json" # Backup file for user account

BACKUP_FILES = {DATADB_FILE: DATADB_BACKUP, ACCOUNTDB_FILE: ACCOUNTDB_BACKUP} # Dictionary to store backup files for each main file

def load_data(filename):
    """
    Safely load a JSON file. 
    If the file is missing or corrupted, return an empty dictionary instead of crashing.
    """
    if not os.path.exists(filename):
        return {}

    try:
        with open(filename, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        # Notify corruption (print in console for testing purposes)
        print(f"WARNING: {filename} is corrupted!!!")

        backup = BACKUP_FILES.get(filename) # Get the backup file for the current file

        if backup and os.path.exists(backup): # If the backup file exists, restore it
            print("Restoring backup...")
            shutil.copy2(backup, filename) # Restore the backup file to the original location

            with open(filename, "r") as f:
                # Try to load the restored file
                return json.load(f)

        return {} # If the backup file is missing or corrupted, return an empty dictionary
    
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return {}
    
def create_backup(original_file, backup_file):
    """Use shutil to copy the original file to a backup location (if it exists)"""
    if os.path.exists(original_file):
        shutil.copy2(original_file, backup_file)

def save_data(data):
    """Save the user data file safely"""
    with open(DATADB_FILE, "w") as f:
        json.dump(data, f, indent=4)

    # Create a backup before overwriting the data file
    create_backup(DATADB_FILE, DATADB_BACKUP)

def get_user_data(username):
    """Load all data and return the specific user's data"""
    data = load_data(DATADB_FILE)

    if username not in data:
        data[username] = {
            "tasks": [],
            "goals": [],
            "habits": [],
            "notebook": [],
            "events": [],
            "flashcards": [],
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

    changed = False # Flag to check if any changes were made

    for key, value in defaults.items():
        # Check if the key is missing in the user's data
        if key not in data[username]:
            data[username][key] = value
            changed = True # Set the flag to True to indicate a change was made

    if changed:
        save_data(data) # Save the updated data to the file

    return data[username] # Return the user's data

def update_user_data(username, user_data):
    """Load all data, update the specific user's data, and save it back to the file"""
    data = load_data(DATADB_FILE)
    data[username] = user_data
    save_data(data)