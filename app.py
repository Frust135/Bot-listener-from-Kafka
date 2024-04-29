import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from conf import DefaultConfig
from routes import kafka_route, bot_route

CONFIG = DefaultConfig()

origins = ["*"]
app = FastAPI(docs_url="/api/v1/docs", redoc_url="/api/v1/redoc")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(kafka_route.router, prefix="/api/kafka")
app.include_router(bot_route.router, prefix="/api/bot")

if __name__ == "__main__":
    uvicorn.run(app, host=CONFIG.HOST, port=CONFIG.PORT)
