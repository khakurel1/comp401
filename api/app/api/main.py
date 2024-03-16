from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as authRouter
from app.api.evaluation import router as evaluationRouter
from app.api.notification import router as notificationRouter
from app.database import engine
from app import model

model.Base.metadata.create_all(bind=engine)
APP = FastAPI()

APP.include_router(authRouter)
APP.include_router(evaluationRouter)
APP.include_router(notificationRouter)


origins = [
    "http://localhost",
    "http://localhost:5173",
]


APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@APP.get("/status", tags=["status"])
async def status() -> dict:
    return {"message": "Server Online!"}
