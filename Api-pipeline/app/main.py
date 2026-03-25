from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.logging import configure_logging
from app.db.bootstrap import initialize_database

configure_logging()

app = FastAPI(title=settings.app_name)
app.include_router(router)


@app.on_event("startup")
def startup_event() -> None:
	initialize_database()
