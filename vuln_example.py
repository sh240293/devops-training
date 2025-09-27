from flask import request
@app.route("/search")
def search():
    query = request.args.get("q")
    return f"Searching for {query}"

