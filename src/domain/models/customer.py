from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .transaction_customer import TransactionCustomer


class Customer(SQLModel, table=True):
    id: Optional[int] = Field(
        description="Unique identifier for the customer", default=None, primary_key=True
    )
    name: str = Field(description="Name of the customer", index=True)
    email: str = Field(description="Email of the customer", unique=True, index=True)
    password: str = Field(description="Hashed password for authentication")

    transactions: List["TransactionCustomer"] = Relationship(back_populates="customer")
