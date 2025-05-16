# backend/app/utils/security.py
from fastapi import HTTPException, status

def verify_token(token: str):
    if token != "fake-jwt-token-demo-only":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": "admin", "role": "admin"}
