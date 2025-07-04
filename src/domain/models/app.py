from typing import Generic, Optional, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class ErrorDetail(BaseModel):
    message: str
    cause: str


class AppResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None
