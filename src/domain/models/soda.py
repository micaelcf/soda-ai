from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .transaction_customer import TransactionCustomer


class Soda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: float
    quantity: int

    transactions: List["TransactionCustomer"] = Relationship(back_populates="soda")
