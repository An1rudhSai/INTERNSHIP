from flask import Flask, render_template, request, jsonify, send_from_directory
from pymongo import MongoClient
import re

app = Flask(__name__, template_folder='vitefront', static_folder='vitefront')

# Connection to MongoDB
client = MongoClient("mongodb://127.0.0.1:27017")
db = client["INTERNSHIP"]


'''@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        day_input = request.form.get("day_input")

        if day_input:
            if day_input in db.list_collection_names():
                collection = db[day_input]
                data = list(collection.find())
                cleaned_data = preprocess_data(data)
                return jsonify({"data": cleaned_data, "selected_day": day_input})
            else:
                return jsonify({"message": "Data not found for the provided date"})

    return render_template("index.html", data=None, selected_day=None)'''

@app.route("/api/data", methods=["GET"])
def get_data():
    day_input = request.args.get("day_input")
    

    if day_input:
        if day_input in db.list_collection_names():
            collection = db[day_input]
            data = list(collection.find())
            cleaned_data = preprocess_data(data)
            return jsonify({"data": cleaned_data, "selected_day": day_input})
        else:
            return jsonify({"message": "Data not found for the provided date"})

    return jsonify({"data": None, "selected_day": None})

def preprocess_data(data):
    cleaned_data = []
    for entry in data:
        cleaned_entry = {
            "header": entry["header"],
            "data": [re.sub(r'\[\d+\]$', '', item) for item in entry["data"]]
        }
        cleaned_data.append(cleaned_entry)
    return cleaned_data

@app.route('/@vite/<path:filename>')
def serve_vite(filename):
    return send_from_directory('./vitefront/dist', filename)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
