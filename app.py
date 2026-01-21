from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Absolute path (IMPORTANT for hosting)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "links.json")

# Create file if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


def load_links():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_links(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/links", methods=["GET"])
def get_links():
    return jsonify(load_links())


@app.route("/add", methods=["POST"])
def add_link():
    data = load_links()
    new_link = {
        "title": request.json.get("title"),
        "url": request.json.get("url")
    }
    data.append(new_link)
    save_links(data)
    return jsonify({"message": "Link added successfully"}), 201


@app.route("/delete", methods=["POST"])
def delete_link():
    index = request.json.get("index")
    data = load_links()

    if 0 <= index < len(data):
        data.pop(index)
        save_links(data)
        return jsonify({"message": "Link deleted"})
    else:
        return jsonify({"error": "Invalid index"}), 400


if __name__ == "__main__":
    app.run()
