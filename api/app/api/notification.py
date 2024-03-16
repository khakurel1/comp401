from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from app.auth.auth_bearer import JWTBearer
from app.database import get_db
import app.model as models
from app.auth.auth_bearer import get_auth_user

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_notifications(
    db: Session = Depends(get_db),
    limit: int = 10,
    page: int = 1,
    user_id: str = Depends(get_auth_user),
    read: bool = False
):
    skip = (page - 1) * limit

    notifications = (
        db.query(models.Notification)
        .filter(models.Notification.user == user_id)
        .filter(models.Notification.read == read)
        # .order_by(models.evaluation.createdAt.desc())
        .limit(limit)
        .offset(skip)
        .all()
    )
    return {
        "status": "success",
        "results": len(notifications),
        "evaluations": notifications,
    }


# TODO: access only own evaluations remaining
@router.get("/{notificationId}", dependencies=[Depends(JWTBearer())])
def notification_detail(
        notificationsId: str, db:
        Session = Depends(get_db),
        user_id: str = Depends(get_auth_user),
):
    notification = (
        db.query(models.Notification)
        .filter(models.Notification.user == user_id)
        .filter(models.Notification.id == notificationsId)
        .first()
    )
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No notification with this id: {id} found",
        )
    return {"status": "success", "notificaiton": notification}


@router.post(
    "/{notificationId}/read",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
)
def read_notification(
    notificationId: str,
    db: Session = Depends(get_db),
):
    notification = (
        db.query(models.Notification)
        .filter(models.Notification.id == notificationId)
        .first()
    )
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No notification with this id: {notificationId} found",
        )
    notification.read = True
    db.add(notification)
    db.commit()
    db.refresh(notification)

    return {"status": "success", "notification": notification}
