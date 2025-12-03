# app.py
import os
import hmac
import hashlib
from flask import Flask, request, abort, jsonify

app = Flask(__name__)

WEBHOOK_SECRET = os.getenv("Divyanshu@26", "")

# Verify GitHub signature
def verify_signature(req):
    signature = req.headers.get("X-Hub-Signature-256")
    if signature is None:
        abort(400, "Missing signature")

    sha_name, signature_hash = signature.split("=")
    if sha_name != "sha256":
        abort(400, "Unsupported hash algorithm")

    mac = hmac.new(WEBHOOK_SECRET.encode(), msg=req.data, digestmod=hashlib.sha256)

    if not hmac.compare_digest(mac.hexdigest(), signature_hash):
        abort(400, "Invalid signature")


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    verify_signature(request)

    event_type = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.get_json()

    print("💬 EVENT RECEIVED:", event_type)

    if event_type == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        number = pr.get("number")

        print(f"📌 PR EVENT: {action} | PR #{number}")

    return jsonify({"status": "ok"}), 200
