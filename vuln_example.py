"""
Secure command execution service.
Provides safe command execution with whitelist validation.
"""
import os
from flask import request, Flask, jsonify

app = Flask(__name__)

# Configuration
ALLOWED_COMMANDS = {
    "ls": "ls -la",
    "pwd": "pwd", 
    "whoami": "whoami",
    "date": "date"
}

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
        # Use os.popen for safer execution with predefined commands
        with os.popen(ALLOWED_COMMANDS[cmd]) as stream:
            result = stream.read()
        return result.strip() or "No output"
    except Exception:
        return "Command execution failed"

@app.route("/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"})

@app.route("/info")
def info():
    """Get system information safely."""
    return jsonify({
        "allowed_commands": list(ALLOWED_COMMANDS.keys()),
        "status": "operational"
    })

if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=5000)

