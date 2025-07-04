from typing import Optional

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from domain.models.app import AppResponse
from domain.models.soda import Soda
from services.soda import soda_service

router = APIRouter(prefix="/soda", tags=["Soda"])


class SodaCreate(BaseModel):
    name: str
    price: float
    quantity: int


class SodaUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None


@router.post("")
def create_soda(soda: SodaCreate):
    return soda_service.create_soda(
        name=soda.name, price=soda.price, quantity=soda.quantity
    )


@router.get("")
def get_sodas():
    return soda_service.get_all_sodas()


@router.get(
    "/{soda_id}",
    responses={status.HTTP_404_NOT_FOUND: {"model": AppResponse[Soda]}},
)
def get_soda(soda_id: int):
    soda_response = soda_service.get_soda_by_id(soda_id)
    if not soda_response.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=soda_response,
        )
    return soda_response


@router.put(
    "/{soda_id}",
    responses={status.HTTP_404_NOT_FOUND: {"model": AppResponse[Soda]}},
)
def update_soda(soda_id: int, soda: SodaUpdate):
    updated_soda_reponse = soda_service.update_soda(
        soda_id=soda_id,
        name=soda.name,
        price=soda.price,
        quantity=soda.quantity,
    )
    if not updated_soda_reponse.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=updated_soda_reponse,
        )
    return updated_soda_reponse


@router.delete(
    "/{soda_id}",
    responses={status.HTTP_404_NOT_FOUND: {"model": AppResponse[bool]}},
)
def delete_soda(soda_id: int):
    success_response = soda_service.delete_soda(soda_id)
    if not success_response.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=success_response,
        )
    return {"detail": "Soda deleted successfully"}


@router.get("/customer/{customer_id}")
def get_sodas_by_customer(customer_id: int):
    return soda_service.get_all_sodas_by_customer_id(customer_id)
