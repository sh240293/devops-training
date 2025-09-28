import subprocess
from flask import request, Flask

app = Flask(__name__)

@app.route("/run")
def run():
    cmd = request.args.get("cmd")
    if cmd == "ls":
        result = subprocess.run(["ls"], capture_output=True, text=True)
        return result.stdout
    return "Command not allowed"

if __name__ == "__main__":
    app.run()

