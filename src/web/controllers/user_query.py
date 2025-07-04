from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from domain.models.action import ActionPlan
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
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": AppResponse[ActionPlan]}
    },
)
def user_query(input: UserQueryInput):
    """
    Endpoint to handle user queries.
    """
    customer_response = customer_service.get_customer_by_id(input.customer_id)
    if not customer_response.data:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=customer_response,
        )
    action_plan_response = user_query_service.get_action_plan(
        customer=customer_response.data, task_description=input.query
    )
    if not action_plan_response.data:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=action_plan_response,
        )
    return action_plan_response
