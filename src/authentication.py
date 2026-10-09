from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt
from src.config import settings

security = HTTPBearer(auto_error=True)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def check_authentication(creds: HTTPAuthorizationCredentials = Depends(security)):
    if settings.debug_apply_any_bearer_tokens:
        return {"user_id": "debug_user"}  # В режиме отладки возвращаем фиктивный user_id
    
    # TODO реализовать всё что ниже
    #creds != None, т.к. auto_error=True, если токен не передан, то будет возвращён 4**
    #user_id = verify_token(creds.credentials)["sub"]
    pass