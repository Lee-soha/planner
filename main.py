from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router
from database.connection import Settings
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
settings = Settings()
origin = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우트 등록
app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")

@app.on_event("startup")
async def init_db():
    await settings.initialize_database()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)