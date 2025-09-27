import os
import sqlite3
from flask import request, Flask

app = Flask(__name__)

# Hardcoded credentials
PASSWORD = "admin123"

# SQL Injection
@app.route("/user/<user_id>")
def get_user(user_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    return str(result)

# Command Injection
@app.route("/run")
def run():
    cmd = request.args.get("cmd")
    os.system(cmd)
    return "Executed"

# Path Traversal
@app.route("/file")
def read_file():
    filename = request.args.get("filename")
    with open(filename, 'r') as f:
        return f.read()

if __name__ == "__main__":
    app.run(debug=True)
