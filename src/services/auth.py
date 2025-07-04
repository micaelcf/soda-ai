from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional
from fastapi import HTTPException, status
import jwt

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from config import CONFIG
from domain.models.customer import Customer
from domain.models.auth import AccessToken, TokenData
from .customer import customer_service, CustomerService
from utils.hash import verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
REFRESH_TOKEN_EXPIRES = timedelta(days=7)
ALGORITHM = "HS256"


class AuthService:
    def __init__(self, customer_service: CustomerService) -> None:
        self.customer_service = customer_service

    def authenticate_user(self, email: str, password: str) -> Optional[Customer]:
        user_response = self.customer_service.get_customer_by_email(email)
        if not user_response.data:
            return None
        if not verify_password(password, user_response.data.password):
            return None
        return user_response.data

    def create_access_token(self, data: TokenData):
        return jwt.encode(
            data.model_dump(), CONFIG.authjwt_secret_key, algorithm="HS256"
        )

    def login(self, email: str, password: str) -> Optional[AccessToken]:
        user = self.authenticate_user(email, password)
        if not user:
            return None
        exp = datetime.now() + ACCESS_TOKEN_EXPIRES
        access_token = self.create_access_token(
            data=TokenData(customer_id=user.id),
        )
        return AccessToken(token=access_token, exp=exp)

    def validate_token(self, token: AccessToken) -> Optional[Customer]:
        if not token.exp:
            return None
        if token.exp < datetime.now():
            return None

        try:
            payload = TokenData(
                **jwt.decode(
                    token.token, CONFIG.authjwt_secret_key, algorithms=ALGORITHM
                )
            )
            id = payload.customer_id
            if id is None:
                return None
        except jwt.InvalidTokenError:
            return None

        customer = self.customer_service.get_customer_by_id(customer_id=id)
        if not customer.data:
            return None

        return customer.data


auth_service = AuthService(customer_service=customer_service)
