from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from pydantic.json_schema import SkipJsonSchema

if TYPE_CHECKING:
    from .transaction_customer import TransactionCustomer


class Soda(SQLModel, table=True):
    id: Optional[int] = Field(
        # OLD: "Incremental ID of the soda, you can reach this number by searching by name and getting the first result"
        # This is confusing for an LLM. It might try to interpret "you can reach..." as a value.
        description="""The unique database identifier for the soda.
        **Instruction:** For CREATE actions, leave this field as `None`. The database will assign it automatically. 
        For READ or UPDATE actions, this field will be populated by the system after finding the soda by name.""",
        default=None,
        primary_key=True,
    )

    name: str = Field(
        # OLD: "Name of the soda, must be in singular"
        # Good, but we can be more directive.
        description="""The standardized, singular name of the soda (e.g., 'Sprite', 'Coca-Cola'). 
        This name MUST be normalized from the user's input based on the provided list of available sodas.""",
        index=True,
    )
    price: float = Field(
        # OLD: "Price of the soda"
        # This is ambiguous. Is it the price to set or the current price?
        description="""The price of a single unit of the soda. 
        For CREATE actions, use the price provided by the user. 
        For READ actions, leave as 0.0 as the system will fetch the current price.""",
    )
    quantity: int = Field(
        # OLD: "Quantity of the soda"
        # Ambiguous. Is this the stock level or the amount to buy?
        description="The total number of this soda available in the machine's inventory (stock level).",
    )

    transactions: List["TransactionCustomer"] = Relationship(back_populates="soda")
