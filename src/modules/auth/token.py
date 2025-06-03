from jose import jwt
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.database.core import DatabaseSession
import os


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def encode_token(payload: dict) -> str:
    """
    Encode a JWT token with the given payload.
    This function uses the secret key and algorithm specified in the environment
    variables to sign the token.
    The payload should contain the necessary information to identify the user
    and any other claims you want to include in the token.

    Args:
        payload (dict): The payload to encode in the JWT token.

    Returns:
        str: The encoded JWT token as a string.
    """
    load_dotenv()

    return jwt.encode(
        payload, key=os.environ.get("SECRET_KEY"), algorithm=os.environ.get("ALGORITHM")
    )


def decode_token(
    db: DatabaseSession, token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    """
    Decode a JWT token and return the payload.
    This function uses the secret key and algorithm specified in the environment
    variables to verify the token's signature and extract the payload.
    The token should be passed as a Bearer token in the Authorization header
    of the request.

    Args:
        db (DatabaseSession): A database session object to interact with the database.
        token (Annotated[str, Depends): The JWT token to decode, passed as a Bearer token

    Returns:
        dict: The decoded payload from the JWT token.
    """
    load_dotenv()

    data = jwt.decode(
        token=token,
        key=os.environ.get("SECRET_KEY"),
        algorithms=[os.environ.get("ALGORITHM")],
    )
    return data


TokenDependency = Annotated[dict, Depends(decode_token)]
