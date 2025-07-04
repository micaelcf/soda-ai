from typing import TYPE_CHECKING, List, Union
from pydantic import BaseModel, Field

# if TYPE_CHECKING:
from .customer import Customer
from .soda import Soda
from .transaction_customer import TransactionCustomer


class Action(BaseModel):
    type: str = Field(
        description="The CRUD operation to perform on the target entity (e.g., CREATE for making a new item, READ for finding an item)."
    )
    target_name: str = Field(
        description="The class name of the entity being targeted, e.g., 'Soda', 'Customer', 'TransactionCustomer'."
    )
    payload: Customer | Soda | TransactionCustomer = Field(
        description="""The data payload for the action. 
        Populate the fields of this entity object based on the user's request, following the specific instructions in each field's description."""
    )


class ActionPlan(BaseModel):
    plan: List[Action] = Field(
        description="""A sequential list of atomic operations required to fulfill the user's request. 
        The system will execute these actions in the provided order. 
        For example, to buy a soda, the plan must first contain a 'READ' action to find the soda by name, followed by a 'CREATE' action for the 'TransactionCustomer' entity.""",
    )
