from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db
from app.auth.auth_handler import signJWT
# This import is used to sign the JSON Web Token (JWT)

from app.schema import UserSchema, UserLoginSchema
# These imports are used to define the input and output data schemas

from app.model import User, get_password_hash, verify_password
# These imports are used to interact with the database and perform password verification

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
# This import is used to define the API routes and their associated tags

@router.post("/signup")
async def create_user(
    payload: UserSchema, db: Session = Depends(get_db)
):
    new_user = User(**payload.dict())
    # This line creates a new User object using the data from the input schema

    new_user.password = get_password_hash(new_user.password)
    # This line hashes the user's password using the get_password_hash function

    db.add(new_user)
    # This line adds the new user to the database

    db.commit()
    # This line commits the changes to the database

    db.refresh(new_user)
    # This line refreshes the object with the updated database information

    return {"status": "success", "jwt": signJWT(str(new_user.id))}
# This function creates a new user and returns a JWT if the user is created successfully

@router.post("/login")
async def user_login(
    payload: UserLoginSchema, db: Session = Depends(get_db)
):
    user_query = db.query(User).filter(
        User.email == payload.email
    )
    # This line queries the database for a user with the specified email

    db_user = user_query.first()
    # This line retrieves the first user from the query result

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with this email: {payload.email} found",
        )
    # This line raises an HTTPException with a 404 status code if the user is not found

    if not verify_password(payload.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provided email and password didnot match",
        )
    # This line raises an HTTPException with a 404 status code if the password is incorrect

    return {
        "status": "success",
        "jwt": signJWT(str(db_user.id)),
    }
# This function logs in an existing user and returns a JWT if the login is successful