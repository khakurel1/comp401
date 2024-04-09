# Import necessary modules and classes
import time
from typing import Dict

import jwt
# from decouple import config


# Define the JWT_SECRET constant for the secret key used to sign and verify JWTs
JWT_SECRET = "secret"


# Define the JWT_ALGORITHM constant for the algorithm used to sign and verify JWTs
JWT_ALGORITHM = "HS256"


# Define a function to generate a token response with an access token
def token_response(token: str):
    return {
        "access_token": token
    }


# Define a function to sign a JWT with a user ID and return the token response
def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


# Define a function to decode a JWT and return the decoded payload
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token["expires"] >= time.time():
            return decoded_token
        else:
            return None
    except Exception as e:
        return {e}