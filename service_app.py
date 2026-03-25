from flask import Flask, request, jsonify
from pathlib import Path

from crypto import decrypt_value, hash_metadata
from logs import init_public_db, log_access
from policy import evaluate_policy
from token_utils import verify_token

app = Flask(__name__)
init_public_db()


BASE = Path(__file__).resolve().parent
PUBLIC_KEY = (BASE / "keys" / "public.pem").read_bytes()

@app.route("/")
def home():
    return "Public Cloud Running"
@app.route("/access-service", methods=["POST"])
def access_service():
    data = request.get_json()

    token = data.get("token")
    device_hash = data.get("device_hash")

    decoded = verify_token(token)

    if not decoded or "error" in decoded:
        return jsonify({"status": "DENIED", "reason": "Invalid Token"}), 401

    return jsonify({"status": "GRANTED"})

@app.route("/verify-access", methods=["POST"])
def verify_access():
    data = request.json

    token = data["token"]
    requested_service = data["service"]
    device_id = data["device_id"]

    try:
        decoded = verify_token(token, PUBLIC_KEY)
        token_device_hash = decoded["device_hash"]

        if token_device_hash != hash_metadata(device_id):
            return jsonify({"access": "DENIED", "reason": "Device mismatch"}), 403


        claims = {
            "isAdult": decrypt_value(decoded["claims"]["isAdult"]),
            "isStudent": decrypt_value(decoded["claims"]["isStudent"]),
            "isHealthEligible": decrypt_value(decoded["claims"]["isHealthEligible"])
        }


        decision = evaluate_policy(requested_service, claims)


        log_access(decoded["duid"], requested_service, decision)

        return jsonify({"access": decision})

    except Exception as e:
        return jsonify({"access": "DENIED", "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)