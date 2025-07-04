from fastapi import APIRouter


router = APIRouter(prefix="/query", tags=["Query"])


@router.post("")
def user_query(query: str):
    """
    Endpoint to handle user queries.
    """
    # Here you would typically process the query, e.g., by calling a service or database
    return {"message": "Query received", "query": query}
