from fastapi import FastAPI
import models

from database import engine
from routers import customer, bill, flower, revenue

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(customer.router, prefix='/customer', tags=["customer"])
app.include_router(bill.router, prefix='/bill',  tags=["bill"])
app.include_router(flower.router, prefix='/flower',  tags=["flower"])
app.include_router(revenue.router, prefix='/revenue', tags=["revenue"])
