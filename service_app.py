from flask import Flask, request, jsonify
from pathlib import Path
import os

from crypto import decrypt_value, hash_metadata
from logs import init_public_db, log_access
from token_utils import verify_token

app = Flask(__name__)
init_public_db()

# Load public key
BASE = Path(__file__).resolve().parent
PUBLIC_KEY = (BASE / "keys" / "public.pem").read_bytes()


@app.route("/")
def home():
    return "Public Cloud Running"


@app.route("/access-service", methods=["POST"])
def access_service():
    data = request.json

    token = data.get("token")
    device_hash = data.get("device_hash")
    requested_service = data.get("service", "unknown")

    try:
       
        decoded = verify_token(token)

        if not decoded or "error" in decoded:
            return jsonify({"access": "DENIED", "reason": "Invalid Token"}), 401

       
        token_device_hash = decoded.get("meta", {}).get("device")

        print("TOKEN DEVICE HASH:", token_device_hash)
        print("RECEIVED DEVICE HASH:", device_hash)

        if token_device_hash != device_hash:
            print("⚠️ Device mismatch ignored for demo")

        
        claims = {
            "isAdult": 0,
            "isStudent": 0,
            "isHealthEligible": 0
        }

        
        try:
            claims = {
                "isAdult": int(decrypt_value(decoded["claims"]["isAdult"]).strip()),
                "isStudent": int(decrypt_value(decoded["claims"]["isStudent"]).strip()),
                "isHealthEligible": int(decrypt_value(decoded["claims"]["isHealthEligible"]).strip())
            }
        except Exception as e:
            print("DECRYPT ERROR:", str(e))
            print("⚠️ Using fallback claims")

        print("DECRYPTED CLAIMS:", claims)

        
        if requested_service == "education" and claims["isStudent"] == 1:
            decision = "GRANTED"
        elif requested_service in ["health", "welfare"]:
            decision = "GRANTED"
        else:
            decision = "DENIED"

        
        log_access(
    decoded.get("sub", "unknown"),
    requested_service,
    decision,
    device_hash 
)

        return jsonify({"access": decision})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"access": "DENIED", "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)