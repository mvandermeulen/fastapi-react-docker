from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import router as api_router
from app.schema import graphql_router


def get_application():
    app = FastAPI(title="FastAPI, Docker and others", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")
    app.include_router(graphql_router, prefix="/graphql", tags=["graphql"])

    return app


app = get_application()
