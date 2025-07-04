from datetime import datetime
from pydantic import BaseModel


class AccessToken(BaseModel):
    token: str
    exp: datetime | None = None


class TokenData(BaseModel):
    customer_id: int | None = None
