from flask import Flask, request, make_response
import sqlite3
import os
import subprocess

app = Flask(__name__)

# ❌ HARDCODED SECRET (SAST)
API_KEY = "HARDCODED_SECRET_123"

# ❌ DEBUG ENABLED (INFO LEAK)
app.config["DEBUG"] = True


@app.route("/")
def index():
    resp = make_response("DevSecOps vulnerable app")

    # ❌ Missing security headers (DAST)
    resp.headers["Server"] = "Werkzeug/3.1.5 Python/3.11.14"
    return resp


@app.route("/user")
def get_user():
    username = request.args.get("username")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # ❌ SQL Injection (SAST + DAST)
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    result = cursor.fetchall()
    conn.close()

    return str(result)


@app.route("/search")
def search():
    query = request.args.get("q", "")

    # ❌ Reflected XSS (DAST)
    return f"<h1>Search results for: {query}</h1>"


@app.route("/cmd")
def run_command():
    cmd = request.args.get("cmd")

    # ❌ Command Injection (SAST + DAST)
    output = subprocess.getoutput(cmd)
    return f"<pre>{output}</pre>"


@app.route("/file")
def read_file():
    filename = request.args.get("name")

    # ❌ Path Traversal
    with open(filename, "r") as f:
        return f.read()


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # ❌ Weak auth logic + plaintext comparison
    if username == "admin" and password == "admin":
        return "Logged in as admin"

    return "Login failed", 401


@app.route("/env")
def env():
    # ❌ Sensitive information disclosure
    return dict(os.environ)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
