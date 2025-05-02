import json
import os

def load_transactions():
    data_path = os.path.join(os.path.dirname(__file__), "data", "transactions.json")
    with open(data_path, "r") as file:
        return json.load(file)
