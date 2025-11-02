from flask import Flask, render_template, request, redirect
from prometheus_flask_exporter import PrometheusMetrics

import json
import os
import psycopg2   # PostgreSQL

app = Flask(__name__)
metrics = PrometheusMetrics(app)

DATA_FILE = "messages.json"

# ---------------------------
# DATABASE CONNECTION (RDS)
# ---------------------------

def get_db_connection():
    """Return PostgreSQL connection if env variables exist, else None."""
    try:
        db_host = os.getenv("DB_HOST")
        db_user = os.getenv("DB_USER")
        db_pass = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        if not all([db_host, db_user, db_pass, db_name]):
            return None

        conn = psycopg2.connect(
            host=db_host,
            user=db_user,
            password=db_pass,
            dbname=db_name
        )
        return conn
    except:
        return None


# ---------------------------
# LOCAL JSON FALLBACK
# ---------------------------

def load_messages_local():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_messages_local(messages):
    with open(DATA_FILE, "w") as f:
        json.dump(messages, f, indent=4)


# ---------------------------
# DATABASE OPERATIONS
# ---------------------------

def load_messages():
    """Load messages from PostgreSQL if available, else from JSON."""
    conn = get_db_connection()
    if conn is None:
        return load_messages_local()

    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, name TEXT, message TEXT);")
    conn.commit()

    cur.execute("SELECT name, message FROM messages ORDER BY id ASC;")
    rows = cur.fetchall()
    conn.close()

    return [{"name": r[0], "message": r[1]} for r in rows]


def save_message(name, message):
    """Save message into PostgreSQL if available, else store in JSON."""
    conn = get_db_connection()
    if conn is None:
        messages = load_messages_local()
        messages.append({"name": name, "message": message})
        save_messages_local(messages)
        return

    cur = conn.cursor()
    cur.execute("INSERT INTO messages (name, message) VALUES (%s, %s)", (name, message))
    conn.commit()
    conn.close()


# ---------------------------
# ROUTES
# ---------------------------

@app.route("/")
def home():
    messages = load_messages()
    return render_template("index.html", messages=messages)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    message = request.form.get("message")

    if name and message:
        save_message(name, message)

    return redirect("/")


# ---------------------------
# METRICS (for Member 4)
# ---------------------------

@app.route("/metrics")
def metrics_custom():
    return f"guestbook_messages_total {len(load_messages())}\n"


# ---------------------------
# RUN APP
# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
