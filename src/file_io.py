import json
import csv
import os

def load_json(filepath: str) -> dict:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: File not found at {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath: str, data: dict) -> None:
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def write_csv(filepath: str, headers: list, rows: list) -> None:
    with open(filepath, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

def read_csv(filepath: str) -> tuple:
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Error: File not found at {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        return list(reader), headers
    
def ensure_dir(directory_path: str) -> None:
    os.makedirs(directory_path, exist_ok=True)