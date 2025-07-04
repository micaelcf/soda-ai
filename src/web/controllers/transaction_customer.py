from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from domain.models.app import AppResponse
from domain.models.transaction_customer import TransactionCustomer
from services.transaction_customer import transaction_service

router = APIRouter(prefix="/transaction", tags=["TransactionCustomer"])


class TransactionCreate(BaseModel):
    customer_id: int
    soda_id: int
    quantity: int


@router.post("")
def create_transaction(transaction: TransactionCreate):
    new_transaction_response = transaction_service.create_transaction(
        customer_id=transaction.customer_id,
        soda_id=transaction.soda_id,
        quantity=transaction.quantity,
    )
    if not new_transaction_response.data:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=new_transaction_response
        )
    return new_transaction_response


@router.get("")
def get_transactions():
    return transaction_service.get_all_transactions()


@router.get(
    "/{transaction_id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": AppResponse[TransactionCustomer | None]}
    },
)
def get_transaction(transaction_id: int):
    transaction_response = transaction_service.get_transaction_by_id(transaction_id)
    if not transaction_response.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=transaction_response
        )

    return transaction_response


@router.put(
    "/{transaction_id}",
    responses={status.HTTP_404_NOT_FOUND: {"model": AppResponse[TransactionCustomer]}},
)
def update_transaction(transaction_id: int, transaction: TransactionCreate):
    updated_transaction_response = transaction_service.update_transaction(
        transaction_id=transaction_id,
        customer_id=transaction.customer_id,
        soda_id=transaction.soda_id,
        quantity=transaction.quantity,
    )
    if not updated_transaction_response.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content=updated_transaction_response
        )
    return updated_transaction_response


@router.delete(
    "/{transaction_id}",
    responses={status.HTTP_404_NOT_FOUND: {"model": AppResponse[bool]}},
)
def delete_transaction(transaction_id: int):
    success_response = transaction_service.delete_transaction(transaction_id)
    if not success_response.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=success_response
        )
    return success_response


@router.get("/customer/{customer_id}")
def get_transactions_by_customer(customer_id: int):
    return transaction_service.get_transactions_by_customer(customer_id)
