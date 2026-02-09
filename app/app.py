from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# NAMJERNO LOŠE - hardkodirani tajni podatak
API_KEY = "HARDCODED_SECRET_123"

@app.route("/")
def index():
    return "DevSecOps vulnerable app"

@app.route("/user")
def get_user():
    username = request.args.get("username")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # NAMJERNO LOŠE - SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)

    result = cursor.fetchall()
    conn.close()

    return str(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
