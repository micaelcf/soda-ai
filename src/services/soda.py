from typing import Optional, Sequence

from sqlmodel import Session, select

from domain.models.app import AppResponse, ErrorDetail
from domain.models.customer import Customer
from domain.models.soda import Soda
from domain.models.transaction_customer import TransactionCustomer
from infra.db.sqlite import get_session


class SodaService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_soda(self, name: str, price: float, quantity: int) -> AppResponse[Soda]:
        try:
            soda = Soda(name=name, price=price, quantity=quantity)
            self.db_session.add(soda)
            self.db_session.commit()
            self.db_session.refresh(soda)
            return AppResponse(data=soda)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_soda_by_id(self, soda_id: int) -> AppResponse[Soda]:
        try:
            soda = self.db_session.get(Soda, soda_id)
            if not soda:
                return AppResponse(
                    error=ErrorDetail(message="Soda not found", cause="not-found")
                )
            return AppResponse(data=soda)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_all_sodas(self) -> AppResponse[Sequence[Soda]]:
        try:
            statement = select(Soda)
            sodas = self.db_session.exec(statement).all()
            return AppResponse(data=sodas)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def update_soda(
        self,
        soda_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        quantity: Optional[int] = None,
    ) -> AppResponse[Soda]:
        try:
            soda_response = self.get_soda_by_id(soda_id)
            if soda_response.error:
                return soda_response

            soda = soda_response.data
            if not soda:
                return soda_response
            if name is not None:
                soda.name = name
            if price is not None:
                soda.price = price
            if quantity is not None:
                soda.quantity = quantity
            self.db_session.add(soda)
            self.db_session.commit()
            self.db_session.refresh(soda)
            return AppResponse(data=soda)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def delete_soda(self, soda_id: int) -> AppResponse[bool]:
        try:
            soda_response = self.get_soda_by_id(soda_id)
            if soda_response.error:
                return AppResponse(data=False, error=soda_response.error)

            soda = soda_response.data
            self.db_session.delete(soda)
            self.db_session.commit()
            return AppResponse(data=True)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_all_sodas_by_customer_id(
        self, customer_id: int
    ) -> AppResponse[Sequence[Soda]]:
        try:
            statement = (
                select(Soda)
                .join(TransactionCustomer)
                .join(Customer)
                .where(Customer.id == customer_id)
            )
            sodas = self.db_session.exec(statement).all()
            return AppResponse(data=sodas)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))


soda_service = SodaService(db_session=next(get_session()))
