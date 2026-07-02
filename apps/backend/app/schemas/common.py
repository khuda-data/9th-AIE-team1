from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from app.core.codes import ErrorCode, SuccessCode

T = TypeVar("T")
M = TypeVar("M")


class ErrorMeta(BaseModel):
    path: str
    timestamp: int


class ApiResponse(BaseModel, Generic[T, M]):
    success: bool
    status: int
    message: str
    data: T | None = None
    code: str | None = None
    meta: M | None = None

    @classmethod
    def ok(cls, success_code: SuccessCode, data: T | None = None) -> "ApiResponse[T, None]":
        return cls(success=True, status=success_code.status, message=success_code.message, data=data)

    @classmethod
    def created(cls, success_code: SuccessCode, data: T) -> "ApiResponse[T, None]":
        return cls(success=True, status=success_code.status, message=success_code.message, data=data)

    @classmethod
    def on_failure(
        cls, error_code: ErrorCode, meta: ErrorMeta | None = None, message: str | None = None
    ) -> "ApiResponse[None, ErrorMeta]":
        return cls(
            success=False,
            status=error_code.status,
            message=message or error_code.message,
            code=error_code.code,
            meta=meta,
        )


class MessageResponse(BaseModel):
    message: str


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
