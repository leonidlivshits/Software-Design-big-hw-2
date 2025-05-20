from fastapi import FastAPI
from app.routes import router
from common.config import settings
import uvicorn

app = FastAPI(title="API Gateway")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)