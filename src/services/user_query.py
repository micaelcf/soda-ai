from typing import Union
import instructor

import google.generativeai as genai

# from google import genai
from pydantic import BaseModel, Field

from config import CONFIG
from domain.models.action import ActionPlan
from domain.models.app import AppResponse, ErrorDetail
from domain.models.customer import Customer
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
        self, customer: Customer, task_description: str
    ) -> AppResponse[ActionPlan]:
        # try:
        available_products_response = self.soda_service.get_all_sodas()
        if not available_products_response.data:
            return AppResponse(error=available_products_response.error)
        system_prompt = get_system_prompt(customer, available_products_response.data)
        action_plan = client.messages.create(
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                # {
                #     "role": "system",
                #     "content": f"""
                #     You are an Soda vending machine assistant for the *{str(customer)}* customer.
                #     Your task is to understand the user's request and generate an action plan to complete it.
                #     Keep your attention in the quatity of the sodas and the necessary information for a transaction.
                #     """,
                # },
                {"role": "user", "content": task_description},
            ],
            response_model=ActionPlan,
            max_retries=3,
        )
        print("Action Plan:", action_plan)
        # except Exception as e:
        #     return AppResponse(
        #         error=ErrorDetail(
        #             message=str(e),
        #             cause="unknown",
        #         )
        #     )
        return AppResponse(data=action_plan)


user_query_service = UserQueryService(
    customer_service=customer_service,
    soda_service=soda_service,
    transaction_customer_service=transaction_service,
)
