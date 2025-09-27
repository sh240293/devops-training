from app import app           # reuse your Flask `app` instance from app.py
from flask import request, make_response
import sqlite3
import subprocess
import os

# 1) Reflected XSS — returns HTML with unescaped user input (flask HTML context)
@app.route("/vuln_xss")
def vuln_xss():
    q = request.args.get("q", "")
    # Vulnerable: directly embedding user input inside an HTML response
    html = f"<html><body>Searching for: {q}</body></html>"
    return make_response(html, 200)

# 2) SQL Injection — unsafe string interpolation into SQL statements
@app.route("/vuln_sql")
def vuln_sql():
    name = request.args.get("name", "")
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users(name TEXT);")
    # Vulnerable: using an f-string / concatenation for SQL
    cur.execute(f"INSERT INTO users(name) VALUES('{name}');")
    conn.commit()
    # Vulnerable: dynamic query string
    cur.execute(f"SELECT * FROM users WHERE name = '{name}';")
    rows = cur.fetchall()
    conn.close()
    return str(rows)

# 3) Command injection / Shell injection — using shell=True with concatenated input
@app.route("/vuln_cmd")
def vuln_cmd():
    cmd = request.args.get("cmd", "")
    # Vulnerable: concatenating user input and using shell=True
    subprocess.call("echo " + cmd, shell=True)
    return "command executed"

# 4) Unsafe eval — arbitrary code execution from user input
@app.route("/vuln_eval")
def vuln_eval():
    expr = request.args.get("expr", "")
    # Vulnerable: evaluating user-supplied expression
    try:
        result = eval(expr)
    except Exception as e:
        result = f"error: {e}"
    return str(result)

# 5) Hardcoded secret — obvious credential in source (secret detection)
API_KEY = "PUT_REAL_SECRET_HERE_1234567890"   # Vulnerable: hardcoded secret
@app.route("/vuln_secret")
def vuln_secret():
    # Just return a hint — scanners flag the constant above
    return "secret present in source"

# 6) SSRF-style pattern — passing user-supplied URL to requests (if requests installed)
# kept as a no-op string to avoid requiring requests in CI; uncomment to test with requests
# import requests
# @app.route("/vuln_ssrf")
# def vuln_ssrf():
#     url = request.args.get("url", "")
#     # Vulnerable: contacting arbitrary user-supplied URL
#     r = requests.get(url, timeout=2, verify=True)
#     return r.text[:200]

