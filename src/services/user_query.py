from typing import Callable, Dict, List, Sequence, Union
import instructor

import google.generativeai as genai

# from google import genai
from pydantic import BaseModel, Field

from config import CONFIG
from domain.models.action import (
    GeneralAction,
    InventoryManagementAction,
    InventoryOperation,
    PurchaseAction,
    TransactionHistoryAction,
    UserActions,
    UserIntent,
)
from domain.models.app import AppResponse, ErrorDetail
from domain.models.customer import CustomerBase, CustomerDb
from domain.models.soda import Soda
from domain.models.transaction_customer import TransactionCustomer
from services.customer import CustomerService, customer_service
from services.soda import SodaService, soda_service
from services.transaction_customer import (
    TransactionCustomerService,
    transaction_service,
)
from utils.prompts import get_system_prompt

genai.configure(api_key=CONFIG.gemini_api_key)  # type: ignore
client = instructor.from_gemini(
    client=genai.GenerativeModel(  # type: ignore
        model_name="models/gemini-2.5-flash",
        # model_name="models/gemini-2.5-pro",
    ),
    mode=instructor.Mode.GEMINI_JSON,
    use_async=False,
)
print("api_key:", CONFIG.gemini_api_key)  # Debugging line to check API key


class UserQueryService:
    def __init__(
        self,
        customer_service: CustomerService,
        soda_service: SodaService,
        transaction_customer_service: TransactionCustomerService,
    ):
        self.customer_service = customer_service
        self.soda_service = soda_service
        self.transaction_customer_service = transaction_customer_service

    def get_action_plan(
        self, customer: CustomerBase, task_description: str
    ) -> AppResponse[UserActions]:
        try:
            available_products_response = self.soda_service.get_all_sodas()
            system_prompt = get_system_prompt()
            action_plans = client.messages.create(
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"""**Available Sodas:**
                        {str(available_products_response.data)}"""
                        + f"""**Current customer:**
                        {str(customer)}""",
                    },
                    {"role": "user", "content": task_description},
                ],
                response_model=UserActions,
                max_retries=3,
            )
        except Exception as e:
            return AppResponse(
                error=ErrorDetail(
                    message=str(e),
                    cause="unknown",
                )
            )
        return AppResponse(data=action_plans)

    def handle_purchase_action(
        self, customer_id: int, action: PurchaseAction
    ) -> AppResponse[TransactionCustomer]:
        soda_response = self.soda_service.get_soda_by_name(action.soda_name)
        if not soda_response.data or not soda_response.data.id:
            return AppResponse(error=soda_response.error)

        return self.transaction_customer_service.create_transaction(
            customer_id=customer_id,
            soda_id=soda_response.data.id,
            quantity=action.quantity,
        )

    def handle_manage_inventory_action(
        self, action: InventoryManagementAction
    ) -> AppResponse[Soda]:
        if not action.soda.name:
            return AppResponse(
                error=ErrorDetail(
                    message="You must know exactly which soda to manage.",
                    cause="validation",
                )
            )

        # Create new soda if it doesn't exist
        if action.operation == InventoryOperation.ADD:
            return self.soda_service.create_soda(
                name=action.soda.name,
                price=action.soda.price if action.soda.price else 0,
                quantity=action.soda.quantity,
            )

        # Read existing soda
        if action.operation == InventoryOperation.READ:
            if not action.soda.id:
                soda_response = self.soda_service.get_soda_by_name(action.soda.name)
                return soda_response
            soda_response = self.soda_service.get_soda_by_id(action.soda.id)
            return soda_response

        # Update existing soda
        if action.operation == InventoryOperation.UPDATE:
            if not action.soda.id:
                return AppResponse(
                    error=ErrorDetail(
                        message="You must know the soda ID to update it.",
                        cause="validation",
                    )
                )
            return self.soda_service.update_soda(
                soda_id=action.soda.id,
                price=action.soda.price if action.soda.price > 0 else None,
                quantity=action.soda.quantity,
            )

        # Remove existing soda
        if not action.soda.id:
            return AppResponse(
                error=ErrorDetail(
                    message="You must know the soda ID to remove it.",
                    cause="validation",
                )
            )

        return self.soda_service.delete_soda(action.soda.id)

    def handle_transaction_history_action(
        self, action: TransactionHistoryAction
    ) -> AppResponse[Sequence[TransactionCustomer]]:
        if not action.customer.id:
            return AppResponse(
                error=ErrorDetail(
                    message="You must know exactly who the customer is for transaction history.",
                    cause="validation",
                )
            )
        history_response = (
            self.transaction_customer_service.get_transactions_by_customer(
                customer_id=action.customer.id
            )
        )
        if not history_response.data:
            return AppResponse(
                error=history_response.error,
            )
        return history_response

    def handle_general_action(self, action: GeneralAction) -> str:
        return action.message

    def execute_actions(
        self, customer_id: int, user_actions: UserActions
    ) -> AppResponse[
        List[
            AppResponse[Soda]
            | AppResponse[TransactionCustomer]
            | AppResponse[Sequence[TransactionCustomer]]
            | AppResponse[str]
        ]
    ]:
        try:
            out: List[
                AppResponse[Soda]
                | AppResponse[TransactionCustomer]
                | AppResponse[Sequence[TransactionCustomer]]
                | AppResponse[str]
            ] = []
            for action in user_actions.actions:
                if isinstance(action, PurchaseAction):
                    purchase_response = self.handle_purchase_action(customer_id, action)
                    out.append(purchase_response)
                elif isinstance(action, InventoryManagementAction):
                    inventory_response = self.handle_manage_inventory_action(action)
                    out.append(inventory_response)
                elif isinstance(action, TransactionHistoryAction):
                    history_response = self.handle_transaction_history_action(action)
                    out.append(history_response)
                else:
                    general_response = self.handle_general_action(action)
                    out.append(AppResponse(data=general_response))
            return AppResponse(data=out)
        except Exception as e:
            return AppResponse(
                error=ErrorDetail(
                    message=str(e),
                    cause="unknown",
                )
            )


user_query_service = UserQueryService(
    customer_service=customer_service,
    soda_service=soda_service,
    transaction_customer_service=transaction_service,
)
