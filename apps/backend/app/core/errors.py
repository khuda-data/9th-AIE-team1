import logging
import time

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.codes import ErrorCode
from app.schemas.common import ApiResponse, ErrorMeta

logger = logging.getLogger(__name__)


class BusinessError(Exception):
    def __init__(self, error_code: ErrorCode, detail: str | None = None):
        message = error_code.message if detail is None else f"{error_code.message} - {detail}"
        super().__init__(message)
        self.error_code = error_code


def _error_meta(request: Request) -> ErrorMeta:
    return ErrorMeta(path=request.url.path, timestamp=int(time.time() * 1000))


def _failure_response(
    request: Request, error_code: ErrorCode, status_code: int, message: str | None = None
) -> JSONResponse:
    body = ApiResponse.on_failure(error_code, meta=_error_meta(request), message=message)
    return JSONResponse(status_code=status_code, content=body.model_dump(exclude_none=True))


async def business_error_handler(request: Request, exc: BusinessError) -> JSONResponse:
    logger.warning("[%s] %s", exc.error_code.code, exc)
    return _failure_response(request, exc.error_code, exc.error_code.status, message=str(exc))


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("request validation failed: %s", exc.errors())
    return _failure_response(
        request, ErrorCode.INVALID_MAPPING_PARAMETER, status.HTTP_400_BAD_REQUEST
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("unhandled exception")
    return _failure_response(
        request,
        ErrorCode.INTERNAL_SERVER_ERROR,
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        message=str(exc),
    )
