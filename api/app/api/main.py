from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as authRouter
from app.api.evaluation import router as evaluationRouter
from app.api.notification import router as notificationRouter
from app.api.ticker import router as tickerRouter
from app.database import engine
from app import model

model.Base.metadata.create_all(bind=engine)
APP = FastAPI()

APP.include_router(authRouter)
APP.include_router(evaluationRouter)
APP.include_router(notificationRouter)
APP.include_router(tickerRouter)


origins = [
    # "http://localhost",
    # "http://localhost:5174",
    # "http://192.168.1.71:5173",
    # "https://96f0-2400-1a00-b060-52b1-3a2f-9dff-75a6-978a.ngrok-free.app/"
    "*"
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
