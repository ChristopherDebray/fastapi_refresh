import logging

from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.core.exceptions.unique_constraint_exceptions import UniqueConstraintException

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "isSuccess": False,
            "path": request.url.path,
            "error": exc.detail,
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "isSuccess": False,
            "path": request.url.path,
            "error": "Internal server error",
        },
    )


async def conflict_exception_handler(request: Request, exc: UniqueConstraintException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "isSuccess": False,
            "path": request.url.path,
            "error": str(exc),
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [
        f"{' -> '.join(str(loc) for loc in err['loc'] if loc != 'body')}: {err['msg']}"
        for err in exc.errors()
    ]
    logger.warning(f"Validation error on {request.url.path}: {errors}")
    return JSONResponse(
        status_code=422,
        content={
            "isSuccess": False,
            "path": request.url.path,
            "error": errors,
        },
    )
