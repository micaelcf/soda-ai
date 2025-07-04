from typing import List, Optional, Sequence

from sqlmodel import Session, select

from domain.models.app import AppResponse, ErrorDetail
from domain.models.customer import Customer
from infra.db.sqlite import get_session
from utils.hash import hash_password


class CustomerService:
    def __init__(self, db_session: Session):
        print("Created CustomerService")
        self.db_session = db_session

    def create_customer(
        self, name: str, email: str, password: str
    ) -> AppResponse[Customer]:
        try:
            existing_customer_response = self.get_customer_by_email(email)
            if existing_customer_response.data:
                return AppResponse(
                    error=ErrorDetail(message="Email already exists", cause="conflict")
                )

            customer = Customer(
                name=name, email=email, password=hash_password(password)
            )
            self.db_session.add(customer)
            self.db_session.commit()
            self.db_session.refresh(customer)
            return AppResponse(data=customer)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_customer_by_id(self, customer_id: int) -> AppResponse[Customer]:
        try:
            customer = self.db_session.get(Customer, customer_id)
            if not customer:
                return AppResponse(
                    error=ErrorDetail(message="Customer not found", cause="not-found")
                )
            return AppResponse(data=customer)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_customer_by_email(self, email: str) -> AppResponse[Customer]:
        try:
            statement = select(Customer).where(Customer.email == email)
            customer = self.db_session.exec(statement).first()
            return AppResponse(data=customer)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def get_all_customers(self) -> AppResponse[Sequence[Customer]]:
        try:
            statement = select(Customer)
            customers = self.db_session.exec(statement).all()
            return AppResponse(data=customers)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def update_customer(
        self, customer_id: int, name: Optional[str] = None, email: Optional[str] = None
    ) -> AppResponse[Customer]:
        try:
            customer_response = self.get_customer_by_id(customer_id)
            if customer_response.error:
                return customer_response

            customer = customer_response.data
            if not customer:
                return customer_response
            if name is not None:
                customer.name = name
            if email is not None:
                customer.email = email
            self.db_session.add(customer)
            self.db_session.commit()
            self.db_session.refresh(customer)
            return AppResponse(data=customer)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))

    def delete_customer(self, customer_id: int) -> AppResponse[bool]:
        try:
            customer_response = self.get_customer_by_id(customer_id)
            if customer_response.error:
                return AppResponse(error=customer_response.error)

            customer = customer_response.data
            self.db_session.delete(customer)
            self.db_session.commit()
            return AppResponse(data=True)
        except Exception as e:
            return AppResponse(error=ErrorDetail(message=str(e), cause="unknown"))


customer_service = CustomerService(db_session=next(get_session()))
