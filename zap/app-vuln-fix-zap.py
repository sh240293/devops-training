from flask import Flask, request, make_response
from markupsafe import escape

app = Flask(__name__, static_folder=None)

@app.after_request
def headers(resp):
    resp.headers.setdefault("X-Content-Type-Options", "nosniff")
    resp.headers.setdefault("X-Frame-Options", "DENY")
    resp.headers.setdefault("Content-Security-Policy", "default-src 'self'")
    return resp

@app.route("/search")
def search():
    q = request.args.get("q", "")
    safe = escape(q)
    return make_response(f"<html><body>You searched for: {safe}</body></html>", 200)

@app.errorhandler(404)
def not_found(e):
    return "Not Found", 404

@app.errorhandler(500)
def internal_error(e):
    return "Internal Server Error", 500

if __name__ == "__main__":
    # Run in production-like mode (debug=False) so flask won't leak internals
    app.run(host="0.0.0.0", port=5000, debug=False)
