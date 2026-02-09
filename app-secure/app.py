from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return "DevSecOps secure app"

@app.route("/user")
def get_user():
    username = request.args.get("username")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchall()
    conn.close()

    return str(result)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    return render_template_string("Search results for: {{ query }}", query=query)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
