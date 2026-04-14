from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.core.exceptions.unique_constraint_exceptions import UniqueConstraintException
from app.core.middleware.exception_handler import generic_exception_handler, http_exception_handler, conflict_exception_handler, validation_exception_handler
from app.core.middleware.response_wrapper import ResponseWrapperMiddleware
from app.routes._system import router as system_router
from app.module.user.presentation.routes import router as user_router
from app.core.config import settings

app = FastAPI(
    title="Fastapi refresh",
    version="1.0.0",
    openapi_version="3.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ResponseWrapperMiddleware)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(UniqueConstraintException, conflict_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(system_router)
app.include_router(user_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}