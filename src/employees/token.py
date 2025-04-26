from jose import jwt
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.database.core import DatabaseSession
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="employees/login")


def encode_token(payload: dict) -> str:
    load_dotenv()

    return jwt.encode(
        payload, key=os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM")
    )


def decode_token(
    db: DatabaseSession, token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    load_dotenv()

    data = jwt.decode(
        token=token,
        key=os.environ.get("SECRET_KEY"),
        algorithms=[os.environ.get("ALGORITHM")],
    )
    return data


TokenDependency = Annotated[dict, Depends(decode_token)]
