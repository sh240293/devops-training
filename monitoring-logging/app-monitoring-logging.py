import logging, sys, json
from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

# Configure logging to stdout
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(message)s"
)

# Define Prometheus counter metric
failed_login_attempts = Counter(
    "login_failed_total",
    "Total number of failed login attempts",
    ["user"]
)

def log_event(event_type, details):
    logging.info(json.dumps({"event": event_type, "details": details}))

@app.route("/login")
def login_attempt():
    user = "admin"
    status = "failed"

    # Log the event
    log_event("login_attempt", {"user": user, "status": status})

    # Update the Prometheus metric
    if status == "failed":
        failed_login_attempts.labels(user=user).inc()

    return "Login failed"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
