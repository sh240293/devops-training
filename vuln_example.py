import os
from flask import request, Flask

app = Flask(__name__)

@app.route("/run")
def run():
    cmd = request.args.get("cmd")
    os.system(cmd)  # Dangerous: CodeQL will flag this
    return "Executed"
