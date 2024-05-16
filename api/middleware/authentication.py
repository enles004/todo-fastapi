from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError, decode

from config import secret_key

oauth_bearer = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def current_user(token: Annotated[str, Depends(oauth_bearer)]):
    try:
        credential = decode(token, secret_key, algorithms="HS2565")
    except ExpiredSignatureError:
        return {"error": "Token has expired"}
    except InvalidTokenError:
        return {"error": "Invalid token"}
    user_id = credential["user_id"]
    email = credential["email"]
    username = credential["username"]
    return {"username": username, "email": email, "user_id": user_id}

