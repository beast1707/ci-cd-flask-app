from flask import Flask, render_template, request, redirect
from prometheus_flask_exporter import PrometheusMetrics

import json
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)



DATA_FILE = "messages.json"

# Load previous messages
def load_messages():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Save new messages
def save_messages(messages):
    with open(DATA_FILE, "w") as f:
        json.dump(messages, f, indent=4)

@app.route("/")
def home():
    messages = load_messages()
    return render_template("index.html", messages=messages)

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    message = request.form.get("message")

    if name and message:
        messages = load_messages()
        messages.append({"name": name, "message": message})
        save_messages(messages)

    return redirect("/")

@app.route("/metrics")
def metrics():
    # dummy metric for Prometheus
    return "guestbook_messages_total {}\n".format(len(load_messages()))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
