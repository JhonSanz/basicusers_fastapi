from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel
from fastapi import status
from fastapi.responses import JSONResponse

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    ok: bool
    msg: Optional[str] = ""
    data: Optional[T] = None


def std_response(
    *,
    status_code,
    ok: bool,
    msg: str,
    data: Optional[T] = None,
):
    content = StandardResponse(ok=ok, msg=msg, data=data).model_dump()
    return JSONResponse(
        status_code=status_code,
        content=content,
    )
