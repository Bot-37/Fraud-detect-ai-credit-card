# app/api/routes/auth.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()

# 🧑 Dummy admin credentials
DUMMY_ADMIN = {
    "username": "admin",
    "password": "admin123",
    "role": "admin"
}

# 📥 Request schema
class LoginRequest(BaseModel):
    username: str
    password: str

# 📤 Response schema (optional, for clarity)
class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

@router.post("/login", response_model=LoginResponse)
def login_user(data: LoginRequest):
    if data.username == DUMMY_ADMIN["username"] and data.password == DUMMY_ADMIN["password"]:
        return {
            "access_token": "fake-jwt-token-demo-only",
            "token_type": "bearer",
            "role": DUMMY_ADMIN["role"]
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )
