from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db
from app.auth.auth_handler import signJWT
from app.auth.auth_bearer import get_auth_user
from app.schema import UserSchema, UserLoginSchema
from app.model import User, get_password_hash, verify_password
from app.auth.auth_bearer import JWTBearer

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get("/current_user", dependencies=[Depends(JWTBearer())])
async def current_user(
        db: Session = Depends(get_db),
        user_id: str = Depends(get_auth_user)
):
    user_query = db.query(User).filter(
        User.id == user_id
    )
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="user not found credentials",
        )
    return {"data": db_user.to_dict()}


@router.post("/signup")
async def create_user(
    payload: UserSchema, db: Session = Depends(get_db)
):
    new_user = User(**payload.dict())
    new_user.password = get_password_hash(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"jwt": signJWT(str(new_user.id))}


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
            status_code=400,
            detail=f"No user with this email: {payload.email} found",
        )

    if not verify_password(payload.password, db_user.password):
        raise HTTPException(
            status_code=400,
            detail="Provided email and password didnot match",
        )

    return {"jwt": signJWT(str(db_user.id))}
