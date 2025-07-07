from enum import Enum
from typing import List, Union
from pydantic import BaseModel, Field

# if TYPE_CHECKING:
from .customer import CustomerBase
from .soda import Soda
from .transaction_customer import TransactionCustomer


class UserIntent(str, Enum):
    PURCHASE = "purchase"
    MANAGE_INVENTORY = "manage_inventory"
    CHECK_TRANSACTIONS_HISTORY = "check_transactions_history"
    GREETING = "greeting"
    UNSUPPORTED = "unsupported"


class PurchaseAction(BaseModel):
    """
    Represents a user's intent to purchase one or more sodas.
    This action is triggered when a user explicitly states they want to buy a product.
    """

    intent: UserIntent = Field(
        UserIntent.PURCHASE,
        description="The user's intent when talking with the vending machine.",
    )
    soda_name: str = Field(
        description="The specific type of soda the user wants to buy. The name should be normalized."
    )
    quantity: int = Field(
        default=1,
        description="The number of sodas the user wants to buy. Defaults to 1 if not specified.",
        ge=1,
    )


# INTENT: MANAGE_INVENTORY (New & Expanded)


class InventoryOperation(str, Enum):
    ADD = "add"
    READ = "read"
    REMOVE = "remove"
    UPDATE = "update"


class InventoryManagementAction(BaseModel):
    intent: UserIntent = Field(
        UserIntent.MANAGE_INVENTORY,
        description="The operator's intent to manage inventory.",
    )
    operation: InventoryOperation = Field(
        description="""The specific inventory operation to perform, such as 'add', 'read', 'remove' or 'update'.
        Consider update if you identify the id of the soda (soda already exists). If you see just a name, consider it an add operation.""",
    )
    soda: Soda = Field(
        description="The soda to manage. This should contain a normalized soda name. If the soda doesn't exist, the quantity and price should be specified. If the soda already exists, you can specify just the name and the id (if you know it).",
    )


# INTENT: CHECK_TRANSACTIONS_HISTORY (New)
class TransactionHistoryAction(BaseModel):
    """
    Represents a user's request to check transaction history.
    This can be for a specific customer or for a specific time frame.
    """

    intent: UserIntent = Field(
        UserIntent.CHECK_TRANSACTIONS_HISTORY,
        description="The user's intent to check transaction history.",
    )
    customer: CustomerBase = Field(
        description="The customer whose transaction history is being requested. If you cannot find the customer_id just get the customer name.",
    )


class GeneralAction(BaseModel):
    """
    A catch-all for general conversation, greetings, or unsupported requests.
    This helps the machine respond gracefully to non-transactional input.
    """

    intent: UserIntent = Field(
        UserIntent.GREETING,
        description="The user's general intent, such as a greeting or an unclear/unsupported request.",
    )
    message: str = Field(
        description="Your polite response to the user's message or a note about the unsupported request."
    )


# This Union type is the key. Instructor will try to parse the user message
# into one of these models.
class UserActions(BaseModel):
    """
    Represents the user's action based on their input.
    This can be a purchase, inventory check, transaction history request, or general conversation.
    """

    actions: List[
        Union[
            PurchaseAction,
            InventoryManagementAction,
            TransactionHistoryAction,
            GeneralAction,
        ]
    ] = Field(
        description="User's actions based on their input. This is a list because the user can ask multiple things at once."
    )
