from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user")
def get_user():
    username = request.args.get("username", "")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Parameterized query (NO SQL injection)
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    result = cursor.fetchall()
    conn.close()

    return render_template("user.html", result=result)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return render_template("search.html", query=query)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
