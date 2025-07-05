from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from web.controllers import customer, user_query, soda, transaction_customer
from infra.db.sqlite import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    print("App start")
    create_db_and_tables()
    yield
    print("App shutdown")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth.router)
app.include_router(customer.router)
app.include_router(soda.router)
app.include_router(transaction_customer.router)
app.include_router(user_query.router)
print("Routers:")
for r in app.routes:

    print("\t" + str(r))


@app.get("/")
async def main():
    return {"message": "Hello World"}
