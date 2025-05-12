# thank u chatgpt

from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DB_FILE = "package_db.json"

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)
    f.flush()

@app.route("/add", methods=["POST"])
def add_package():
    data = request.get_json()
    if not data or "name" not in data or "url" not in data:
        return jsonify({"error": "Missing required keys (name, url.)"}), 400

    db = load_db()
    name = data["name"]

    db[name] = {
        "url": data["url"],
        "deps": data.get("deps", data.get("simplepm", [])),
        "pypi": data.get("pypi", []),
        "other": data.get("other", [])
    }

    save_db(db)
    return jsonify({"message": f"Package '{name}' added."}), 200

@app.route("/list", methods=["GET"])
def list_packages():
    db = load_db()
    return jsonify(db)

if __name__ == "__main__":
    app.run(port=5000)
