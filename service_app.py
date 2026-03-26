used_tokens = set()
from flask import Flask, request, jsonify
from pathlib import Path
import os

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
    data = request.json

    token = data["token"]
    device_hash = data["device_hash"]
    requested_service = data.get("service", "unknown")

    try:
        decoded = verify_token(token)

       # if token in used_tokens:
             #return jsonify({
                  #"access": "DENIED",
                  #"reason": "Replay attack detected"
                 # }), 403
        #used_tokens.add(token)

        if not decoded or "error" in decoded:
            return jsonify({"access": "DENIED", "reason": "Invalid Token"}), 401


        token_device_hash = decoded["meta"]["device"]

        if token_device_hash != device_hash:
            return jsonify({"access": "DENIED", "reason": "Device mismatch"}), 403

        
        claims = {
            "isAdult": decrypt_value(decoded["claims"]["isAdult"]),
            "isStudent": decrypt_value(decoded["claims"]["isStudent"]),
            "isHealthEligible": decrypt_value(decoded["claims"]["isHealthEligible"])
        }

        
        decision = evaluate_policy(requested_service, claims)

        log_access(decoded["sub"], requested_service, decision)

        return jsonify({"access": decision})

    except Exception as e:
        return jsonify({"access": "DENIED", "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)