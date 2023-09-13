import json


def load_data():
    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty dictionary if data file doesn't exist or is corrupted

def save_data(data):
    with open('users.json', 'w') as file:
        if (data):
            json.dump(data, file)
