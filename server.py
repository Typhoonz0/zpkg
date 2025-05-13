from flask import Flask, request, jsonify

app = Flask(__name__)
db = {}  # In-memory database

@app.route("/add", methods=["POST"])
def add_package():
    data = request.get_json()
    if not data or "name" not in data or "url" not in data:
        return jsonify({"error": "Missing required keys (name, url.)"}), 400

    name = data["name"]

    db[name] = {
        "url": data["url"],
        "deps": data.get("deps", data.get("simplepm", [])),
        "pypi": data.get("pypi", []),
        "other": data.get("other", [])
    }

    return jsonify({"message": f"Package '{name}' added."}), 200

@app.route("/list", methods=["GET"])
def list_packages():
    return jsonify(db)

if __name__ == "__main__":
    app.run(port=5000)
