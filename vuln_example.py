"""
Secure command execution service.
Provides safe command execution with whitelist validation.
"""
import subprocess
from flask import request, Flask, jsonify

app = Flask(__name__)

# Configuration
ALLOWED_COMMANDS = ["ls", "pwd", "whoami"]

@app.route("/")
def home():
    """Home endpoint returning welcome message."""
    return "Hello, Secure World!"

@app.route("/run")
def run():
    """
    Execute allowed commands safely.
    
    Args:
        cmd (str): Command to execute (must be in whitelist)
    
    Returns:
        str: Command output or error message
    """
    cmd = request.args.get("cmd")
    
    # Input validation
    if not cmd:
        return "No command provided"
    
    # Check if command is allowed
    if cmd not in ALLOWED_COMMANDS:
        return "Command not allowed"
    
    try:
        # Execute command safely
        result = subprocess.run(
            [cmd], 
            capture_output=True, 
            text=True, 
            timeout=5,
            check=False
        )
        return result.stdout or result.stderr
    except subprocess.TimeoutExpired:
        return "Command timed out"
    except Exception:
        return "Command execution failed"

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)

