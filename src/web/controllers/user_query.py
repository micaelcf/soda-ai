from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from domain.models.action import UserActions
from domain.models.app import AppResponse
from services.user_query import user_query_service
from services.customer import customer_service


router = APIRouter(prefix="/query", tags=["Query"])


class UserQueryInput(BaseModel):
    """
    Model for user query input.
    """

    customer_id: int
    query: str


@router.post(
    "",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": AppResponse[UserActions]}
    },
)
def user_query_handler(input: UserQueryInput):
    """
    Endpoint to handle user queries.
    """
    customer_response = customer_service.get_customer_by_id(input.customer_id)
    if not customer_response.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(customer_response),
        )
    action_plan_response = user_query_service.get_action_plan(
        customer=customer_response.data, task_description=input.query
    )
    if not action_plan_response.data:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(action_plan_response),
        )
    return action_plan_response


@router.post(
    "/actions",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": AppResponse[UserActions]}
    },
)
def user_actions_handler(input: UserQueryInput):
    """
    Endpoint to handle user actions.
    """
    customer_response = customer_service.get_customer_by_id(input.customer_id)
    if not customer_response.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=jsonable_encoder(customer_response),
        )
    action_plan_response = user_query_service.get_action_plan(
        customer=customer_response.data, task_description=input.query
    )
    if not action_plan_response.data:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(action_plan_response),
        )
    # Execute the actions
    action_plan_executed_response = user_query_service.execute_actions(
        customer_id=input.customer_id, user_actions=action_plan_response.data
    )
    return action_plan_executed_response
