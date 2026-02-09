from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return "DevSecOps secure app"

@app.route("/user")
def get_user():
    username = request.args.get("username")

    # Sigurno korištenje parametriziranih SQL upita
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchall()
    conn.close()

    return str(result)

@app.route("/search")
def search():
    query = request.args.get("q", "")
    # Sigurno korištenje render_template_string kako bi se izbjegao XSS
    safe_html = render_template_string("Search results for: {{ query }}", query=query)
    return safe_html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
