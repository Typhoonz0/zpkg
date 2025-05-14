from flask import Flask, request, jsonify
import json
import os
import hashlib

app = Flask(__name__)
DB_FILE = "/data/package_db.json"  # Persisted to volume

def hash_secret(secret):
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

@app.route("/add", methods=["POST"])
def add_package():
    data = request.get_json()
    if not data or "name" not in data or "url" not in data or "secret" not in data:
        return jsonify({"error": "Missing required keys (name, url, secret)."}), 400

    db = load_db()
    name = data["name"]

    if name in db:
        return jsonify({"error": f"Package '{name}' already exists."}), 409

    hashed_secret = hash_secret(data["secret"])
    db[name] = {
        "url": data["url"],
        "deps": data.get("deps", data.get("simplepm", [])),
        "pypi": data.get("pypi", []),
        "other": data.get("other", []),
        "uploaded_by": hashed_secret
    }

    save_db(db)
    return jsonify({"message": f"Package '{name}' added."}), 200

@app.route("/list", methods=["GET"])
def list_packages():
    db = load_db()
    return jsonify(db)

@app.route("/remove", methods=["POST"])
def remove_package():
    data = request.get_json()
    if not data or "name" not in data or "secret" not in data:
        return jsonify({"error": "Missing required keys (name, secret)."}), 400

    name = data["name"]
    provided_hash = hash_secret(data["secret"])

    db = load_db()

    if name not in db:
        return jsonify({"error": f"Package '{name}' not found."}), 404

    if db[name].get("uploaded_by") != provided_hash:
        return jsonify({"error": "Unauthorized. You can only remove packages you uploaded."}), 403

    del db[name]
    save_db(db)

    return jsonify({"message": f"Package '{name}' removed."}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
