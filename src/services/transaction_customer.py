from typing import Sequence

from sqlmodel import Session, select

from domain.models.app import AppResponse, ErrorDetail
from domain.models.transaction_customer import TransactionCustomer
from infra.db.sqlite import get_session
from services.soda import SodaService, soda_service
from services.customer import CustomerService, customer_service


class TransactionCustomerService:
    def __init__(
        self,
        db_session: Session,
        soda_service: SodaService,
        customer_service: CustomerService,
    ):
        self.db_session = db_session
        self.soda_service = soda_service
        self.customer_service = customer_service

    def create_transaction(
        self, customer_id: int, soda_id: int, quantity: int
    ) -> AppResponse[TransactionCustomer]:
        try:
            customer_response = self.customer_service.get_customer_by_id(customer_id)
            if not customer_response.data:
                return AppResponse(error=customer_response.error)
            soda_response = self.soda_service.get_soda_by_id(soda_id)
            if soda_response.error:
                return AppResponse(error=soda_response.error)

            soda = soda_response.data
            if not soda:
                return AppResponse(
                    error=ErrorDetail(message="Soda not found", cause="not-found")
                )
            if soda.quantity < quantity:
                return AppResponse(
                    error=ErrorDetail(
                        message="Insufficient soda quantity", cause="conflict"
                    )
                )

            self.soda_service.update_soda(soda_id, quantity=soda.quantity - quantity)

            transaction = TransactionCustomer(
                customer_id=customer_id, soda_id=soda_id, quantity=quantity
            )
            self.db_session.add(transaction)
            self.db_session.commit()
            self.db_session.refresh(transaction)
            return AppResponse(data=transaction)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def update_transaction(
        self, transaction_id: int, customer_id: int, soda_id: int, quantity: int
    ) -> AppResponse[TransactionCustomer]:
        try:
            soda_response = self.soda_service.get_soda_by_id(soda_id)

            soda = soda_response.data
            if not soda:
                return AppResponse(error=soda_response.error)
            if soda.quantity < quantity:
                return AppResponse(
                    error=ErrorDetail(
                        message="Insufficient soda quantity", cause="conflict"
                    )
                )

            self.soda_service.update_soda(soda_id, quantity=quantity)

            transaction = self.db_session.get(TransactionCustomer, transaction_id)
            if not transaction:
                return AppResponse(
                    error=ErrorDetail(
                        message="Transaction not found", cause="not-found"
                    )
                )

            transaction.customer_id = customer_id
            transaction.soda_id = soda_id
            transaction.quantity = quantity
            self.db_session.add(transaction)
            self.db_session.commit()
            self.db_session.refresh(transaction)
            return AppResponse(data=transaction)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_transaction_by_id(
        self, transaction_id: int
    ) -> AppResponse[TransactionCustomer]:
        try:
            transaction = self.db_session.get(TransactionCustomer, transaction_id)
            if not transaction:
                return AppResponse(
                    error=ErrorDetail(
                        message="Transaction not found", cause="not-found"
                    )
                )
            return AppResponse(data=transaction)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_all_transactions(self) -> AppResponse[Sequence[TransactionCustomer]]:
        try:
            statement = select(TransactionCustomer)
            transactions = self.db_session.exec(statement).all()
            return AppResponse(data=transactions)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_transactions_by_customer(
        self, customer_id: int
    ) -> AppResponse[Sequence[TransactionCustomer]]:
        try:
            statement = select(TransactionCustomer).where(
                TransactionCustomer.customer_id == customer_id
            )
            transactions = self.db_session.exec(statement).all()
            return AppResponse(data=transactions)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def delete_transaction(self, transaction_id: int) -> AppResponse[bool]:
        try:
            transaction = self.db_session.get(TransactionCustomer, transaction_id)
            if not transaction:
                return AppResponse(
                    error=ErrorDetail(
                        message="Transaction not found", cause="not-found"
                    )
                )
            self.db_session.delete(transaction)
            self.db_session.commit()
            return AppResponse(data=True)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))


transaction_service = TransactionCustomerService(
    db_session=next(get_session()),
    soda_service=soda_service,
    customer_service=customer_service,
)
