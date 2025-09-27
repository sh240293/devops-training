from app import app
from flask import request

@app.route("/vuln_xss")
def vuln_xss():
    query = request.args.get("q", "")
    # Vulnerable: directly embedding user input in HTML response
    return f"<html><body>Searching for {query}</body></html>"
