from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db
from app.auth.auth_handler import signJWT
from app.schema import UserSchema, UserLoginSchema
from app.model import User, get_password_hash, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/signup")
async def create_user(
    payload: UserSchema, db: Session = Depends(get_db)
):
    new_user = User(**payload.dict())
    new_user.password = get_password_hash(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"status": "success", "jwt": signJWT(str(new_user.id))}


@router.post("/login")
async def user_login(
    payload: UserLoginSchema, db: Session = Depends(get_db)
):
    user_query = db.query(User).filter(
        User.email == payload.email
    )
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No user with this email: {payload.email} found",
        )

    if not verify_password(payload.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Provided email and password didnot match",
        )

    return {
        "status": "success",
        "jwt": signJWT(str(db_user.id)),
    }
