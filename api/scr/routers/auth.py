from datetime import datetime, timedelta
from typing import Annotated

import bcrypt
import jwt
from bson import ObjectId
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from api.schema.schema_auth import RegisterPayload
from config import secret_key
from db.session import users
from tasks import send_telegram, send_mail_register

router = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/auth/register")
async def register(payload: Annotated[RegisterPayload, Body(embed=True)]):
    check_mail = users.find_one({"email": payload.email})
    if check_mail is not None:
        return {"Message": "Email is taken"}

    byte = payload.password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(byte, salt)
    user = {"_id": str(ObjectId()), "username": payload.username, "email": payload.email,
            "password": hashed_password,
            "created": datetime.now(), "role": "user"}
    try:
        users.insert_one(user)
    except Exception:
        return {"Message": "not successfully"}

    data = {'email': user["email"], 'username': user["username"]}
    send_telegram.delay("Hello {}, welcome to my app. (::".format(user["email"]))
    send_mail_register.delay(data)
    return {"message": "created", "data": [{"email": user["email"],
                                            "username": user["username"]}]}


@router.post("/auth/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = users.find_one({"email": form_data.username})
    if not user:
        return {"Message": "Invalid credentials"}
    input_password = form_data.password.encode("utf-8")
    is_correct_password = bcrypt.checkpw(input_password, user["password"])
    if not is_correct_password:
        return {"Message": "Invalid credentials"}

    expiration = datetime.now() + timedelta(minutes=30)
    token = jwt.encode({"user_id": user["_id"],
                        "email": user["email"],
                        "username": user["username"],
                        "exp": expiration},
                       secret_key)

    return {"access_token": token, "token_type": "bearer"}
