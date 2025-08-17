import os, json, httpx
from fastapi import Header, HTTPException, Depends
from jose import jwt
from functools import lru_cache

ISSUER = os.getenv("OIDC_ISSUER", "http://keycloak:8080/realms/drive")
AUDIENCE = os.getenv("JWT_AUDIENCE","drive-web")

@lru_cache(maxsize=1)
def jwks():
    url = f"{ISSUER}/protocol/openid-connect/certs"
    r = httpx.get(url, timeout=5.0)
    r.raise_for_status()
    return r.json()

def verify_jwt(auth_header: str = Header(..., alias="Authorization")):
    if not auth_header.startswith("Bearer "):
        raise HTTPException(401, "Missing bearer token")
    token = auth_header.split(" ",1)[1]
    try:
        header = jwt.get_unverified_header(token)
        key = next(k for k in jwks()["keys"] if k["kid"] == header["kid"])
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key))
        claims = jwt.decode(token, public_key, algorithms=["RS256"], audience=AUDIENCE, options={"verify_at_hash": False})
        if claims.get("iss") and not claims["iss"].startswith(ISSUER):
            raise HTTPException(401, "Invalid issuer")
        return claims
    except Exception as e:
        raise HTTPException(401, f"Invalid token: {e}")

auth_dep = Depends(verify_jwt)
