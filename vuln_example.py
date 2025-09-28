"""
Secure command execution service.
Provides safe command execution with whitelist validation.
"""
import os
from flask import request, Flask, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Security configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = 3600

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

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
@limiter.limit("10 per minute")
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

