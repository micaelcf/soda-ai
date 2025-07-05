from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel
from pydantic.json_schema import SkipJsonSchema

if TYPE_CHECKING:
    from .customer import CustomerDb
    from .soda import Soda


class TransactionCustomer(SQLModel, table=True):
    id: Optional[int] = Field(
        description="The unique database ID for this transaction. The system will generate this.",
        default=None,
        primary_key=True,
    )
    timestamp: datetime = Field(
        description="The timestamp of when the transaction was created. The system will set this.",
        default_factory=datetime.now,
    )

    quantity: int = Field(
        # OLD: "Quantity of the soda to be purchased, when creating a transaction must be filled."
        # Good, but let's be more direct.
        description="The exact number of units the user wants to purchase. This should be extracted directly from the user's request (e.g., '3' from 'buy 3 cokes').",
        ge=1,  # ge=1 is better than ge=0 for a purchase
    )

    soda_id: Optional[int] = Field(
        # OLD: "ID of the soda being purchased"
        # Critical instruction needed here.
        description="""**Instruction:** Leave this field as `None`.
        This is the foreign key for the soda being purchased. The system will populate this field automatically after executing a `READ` action to find the soda by name.""",
        default=None,
        foreign_key="soda.id",
    )

    # ... customer_id has a similar pattern ...
    customer_id: Optional[int] = Field(
        description="""**Instruction:** Leave this field as `None`.
        This is the foreign key for the customer. The system will populate this after identifying the customer.""",
        default=None,
        foreign_key="customer.id",
    )

    soda: "Soda" = Relationship(back_populates="transactions")
    customer: "CustomerDb" = Relationship(back_populates="transactions")
