from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

router = APIRouter()

DUMMY_ADMIN = {
    "username": "admin",
    "password": "admin123",
    "role": "admin"
}

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str

security = HTTPBearer()

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

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token != "fake-jwt-token-demo-only":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return {"username": "admin", "role": "admin"}
