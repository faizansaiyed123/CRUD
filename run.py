import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.configs.utilites import execute_sql_files
from src.routers.users import router as auth_router
from src.routers.posts import router as post_router
from src.routers.likes import router as likes_router
from src.routers.comments import router as comments_router
from fastapi.openapi.utils import get_openapi


def configure_routes(app: FastAPI) -> None:
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(post_router, prefix="/posts", tags=["Posts"])
    app.include_router(likes_router, prefix="/likes", tags=["Likes"])
    app.include_router(comments_router, prefix="/comments", tags=["Comments"])

def create_app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    configure_routes(app)
    
    @app.on_event("startup")
    async def startup_event():
        execute_sql_files()

    return app


app = create_app()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Focus API",
        version="1.0.0",
        description="Secure JWT-authenticated API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {"type": "http", "scheme": "bearer"}
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"HTTPBearer": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi