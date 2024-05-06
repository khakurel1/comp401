from fastapi import Depends, APIRouter, status, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.auth.auth_bearer import JWTBearer
from app.database import get_db
import app.model as models
from app.auth.auth_bearer import get_auth_user
import app.schema as schemas
from app.worker import run_calculations

router = APIRouter(
    prefix="/evaluations",
    tags=["evaluations"]
)


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_evaluations(
    db: Session = Depends(get_db),
    limit: int = 10,
    page: int = 1,
    user_id: str = Depends(get_auth_user),
):
    skip = (page - 1) * limit

    evaluations = (
        db.query(models.Evaluation)
        .filter(models.Evaluation.user == user_id)
        .order_by(models.Evaluation.createdAt.desc())
        .limit(limit)
        .offset(skip)
        .all()
    )

    data = [eval.to_dict() for eval in evaluations]
    return {
        "data": data,
    }


# TODO: access only own evaluations remaining
@router.get("/{evaluationId}", dependencies=[Depends(JWTBearer())])
def evaluation_detail(evaluationId: str, db: Session = Depends(get_db)):
    evaluation = (
        db.query(models.Evaluation)
        .filter(models.Evaluation.id == evaluationId)
        .first()
    )
    if not evaluation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No evaluation with this id: {id} found",
        )
    return {"data": evaluation.to_dict(with_rel=True)}


@router.get("/{evaluationId}/done", dependencies=[Depends(JWTBearer())])
def check_if_done(evaluationId: str, db: Session = Depends(get_db)):
    job = (
        db.query(models.Job)
        .filter(models.Job.evaluation == evaluationId)
        # .order_by(models.evaluation.createdAt.desc())
        .first()
    )

    return {
        "data": job.to_dict(),
    }


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(JWTBearer())],
)
def create_evaluation(
    payload: schemas.CreateEvaluationSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_auth_user),
):
    new_eval = models.Evaluation(**payload.dict(), user=user_id)
    db.add(new_eval)
    db.commit()

    new_job = models.Job(evaluation=new_eval.id)
    db.add(new_job)
    db.commit()

    db.refresh(new_eval)
    background_tasks.add_task(
        run_calculations, new_job.id, user_id, payload.tickers)

    return {
        "message": "evaluation created successfully.",
        "data": new_eval.to_dict()
    }


@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_evaluation(
    evaluation_id: str,
    db: Session = Depends(get_db),
):
    db.query(models.Evaluation).filter(
        models.Evaluation.id == evaluation_id).delete()

    db.commit()
    return {
        "message": f"evaluation {evaluation_id} deleted successfully.",
    }
