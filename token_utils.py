import jwt
from pathlib import Path

# Correct base path (clean)
BASE = Path(__file__).resolve().parent

# Load ONLY public key
PUBLIC_KEY = (BASE / "keys" / "public.pem").read_bytes()


def verify_token(token: str):
    try:
        decoded = jwt.decode(
            token,
            PUBLIC_KEY,
            algorithms=["RS256"]
        )
        return decoded
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}