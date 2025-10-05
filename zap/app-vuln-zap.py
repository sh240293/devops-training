from flask import Flask, request

app = Flask(__name__)

@app.route("/search")
def search():
    q = request.args.get("q", "")
    # INTENTIONALLY vulnerable: reflected XSS (do NOT use in production)
    return f"<html><body>You searched for: {q}</body></html>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
