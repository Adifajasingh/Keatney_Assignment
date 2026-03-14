
from fastapi import FastAPI
from app.api.routes import router
from app.logger import init_db

app = FastAPI(title="Hybrid Search API")

init_db()

app.include_router(router)
