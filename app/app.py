from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.after_request
def add_security_headers(response):
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user")
def get_user():
    username = request.args.get("username", "")

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username FROM users WHERE username = ?",
            (username,)
        )
        result = cursor.fetchall()

    return render_template("user.html", result=result)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return render_template("search.html", query=query)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
