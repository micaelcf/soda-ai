from datetime import datetime
from fastapi import APIRouter, HTTPException, Security, status
from pydantic import BaseModel

from domain.models.auth import AccessToken, TokenData
from services.auth import auth_service, REFRESH_TOKEN_EXPIRES


router = APIRouter(prefix="/auth", tags=["Auth"])


class LoginInputDTO(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login_for_access_token(
    form_data: LoginInputDTO,
) -> AccessToken:
    token = auth_service.login(form_data.email, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/refresh")
def refresh(
    token: AccessToken,
) -> AccessToken:
    """Return a new access token from a refresh token."""
    customer = auth_service.validate_token(token)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    refresh_token = auth_service.create_access_token(
        data=TokenData(customer_id=customer.id)
    )
    return AccessToken(
        token=refresh_token,
        exp=datetime.now() + REFRESH_TOKEN_EXPIRES,
    )
