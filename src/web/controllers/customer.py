import json
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from domain.models.app import AppResponse
from services.customer import customer_service


router = APIRouter(prefix="/customer", tags=["Customer"])


class CustomerCreate(BaseModel):
    name: str
    email: str
    password: str


class CustomerCreatedResponse(BaseModel):
    id: int | None


@router.post(
    "", responses={status.HTTP_400_BAD_REQUEST: {"model": CustomerCreatedResponse}}
)
def create_customer(customer: CustomerCreate):
    customer_create_response = customer_service.create_customer(
        name=customer.name, email=customer.email, password=customer.password
    )
    if not customer_create_response.data:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(customer_create_response),
        )
    return AppResponse(
        data=CustomerCreatedResponse(id=customer_create_response.data.id)
    )


@router.get("")
def get_customers():
    return customer_service.get_all_customers()


@router.get("/{customer_id}")
def get_customer(customer_id: int):
    customer = customer_service.get_customer_by_id(customer_id)
    if not customer.data:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=customer)
    return customer


@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: CustomerCreate):
    updated_customer = customer_service.update_customer(
        customer_id=customer_id,
        name=customer.name,
        email=customer.email,
    )
    if not updated_customer.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=updated_customer
        )
    return updated_customer


@router.delete("/{customer_id}")
def delete_customer(customer_id: int):
    success = customer_service.delete_customer(customer_id)
    if not success.data:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=success)
    return success
