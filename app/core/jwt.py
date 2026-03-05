# security.py
import datetime
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from beanie import PydanticObjectId
from app.core.config import config

# These would ideally be loaded from environment variables
ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()

class DecodedAccessToken(BaseModel):
    exp: int
    id: PydanticObjectId

def create_access_token(data: dict, expires_delta: datetime.timedelta = None) -> str:
    """Creates a JWT token."""
    to_encode = data.copy()
    
    if not expires_delta:
        expires_delta = datetime.timedelta(days=30)
        
    expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    
    return jwt.encode(to_encode, config.JWT_SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> DecodedAccessToken:
    """Dependency to extract and validate the current user from the token."""
    try:
        payload = jwt.decode(credentials.credentials, config.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return DecodedAccessToken(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")