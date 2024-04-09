# Import necessary modules and classes
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from .auth_handler import decodeJWT
from typing import Annotated


# Define a custom JWT bearer class that inherits from the built-in HTTPBearer class
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                # Raise an HTTPException with a status code of 403 and a detail message indicating an invalid authentication scheme
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                    )
            if not self.verify_jwt(credentials.credentials):
                # Raise an HTTPException with a status code of 403 and a detail message indicating an invalid token or expired token
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                    )
            return credentials.credentials
        else:
            # Raise an HTTPException with a status code of 403 and a detail message indicating an invalid authorization code
            raise HTTPException(
                status_code=403, detail="Invalid authorization code."
                )

    def verify_jwt(self, jwtoken: str) -> bool:
        # Define a method to verify the JWT token. If the token is valid, return True; otherwise, return False
        isTokenValid: bool = False

        try:
            # Decode the JWT token using the decodeJWT function from the auth_handler module
            payload = decodeJWT(jwtoken)
        except:
            # If an exception occurs during token decoding, set isTokenValid to False and return False
            payload = None
        if payload:
            # If the token decoding is successful, set isTokenValid to True and return True
            isTokenValid = True
        return isTokenValid


# Define a function to retrieve the user ID from a token using the JWTBearer class
def get_auth_user(token: Annotated[str, Depends(JWTBearer())]) -> str:
    # Define a function to retrieve the user ID from a token. This function uses the JWTBearer class to validate the token
    try:
        # Decode the JWT token using the decodeJWT function from the auth_handler module
        claims = decodeJWT(token)
        # Yield the user ID from the decoded token payload
        yield claims["user_id"]
    except Exception:
        # If an exception occurs during token decoding, return an empty dictionary
        return {}