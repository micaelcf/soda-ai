from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .customer import Customer
    from .soda import Soda


class TransactionCustomer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int
    timestamp: datetime = Field(default_factory=datetime.now)

    soda_id: Optional[int] = Field(default=None, foreign_key="soda.id")
    soda: "Soda" = Relationship(back_populates="transactions")

    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    customer: "Customer" = Relationship(back_populates="transactions")
