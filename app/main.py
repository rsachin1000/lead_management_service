import os
import uvicorn

from fastapi import FastAPI
from dotenv import load_dotenv

from app.apis import router
from app.database import db, DBConfig


load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(title="Lead Management API")
    
    config = DBConfig(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT")),
        db_name=os.getenv("DB_NAME"),
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    
    # Initialize database with the config parameters
    db.init_app(config)
    
    # Add router to the app
    app.include_router(router, prefix="/api/v1", tags=["api"])
    
    return app


app = create_app()
uvicorn.run(
    app, 
    host=os.environ.get("SERVER_HOST"), 
    port=int(os.environ.get("SERVER_PORT"))
)

