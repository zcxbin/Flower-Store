from fastapi import APIRouter, Path, status, Query
from dependency import db_dependency
import crud
from schemas import CustomerRequest
from modify import sum_total_bill, set_customer_level

router = APIRouter()


@router.get("/get_customer", status_code=status.HTTP_200_OK)
async def get_customer(db: db_dependency):
    sum_total_bill(db)
    set_customer_level(db)
    customers = crud.get_customers(db)

    return customers


@router.get("/get_customer/{customer_id}", status_code=status.HTTP_200_OK)
async def get_customer_by_id(db: db_dependency, customer_id: int = Path(gt=0)):
    return crud.get_customer_by_id(db, customer_id)


@router.get("/get_customer_by_level", status_code=status.HTTP_200_OK)
async def get_customer_by_level(db: db_dependency, level_id: int = Query(gt=0)):
    return crud.get_customer_by_level(db, level_id)


@router.get("/get_customer_by_month_and_year", status_code=status.HTTP_200_OK)
async def get_customer_by_month(db: db_dependency, month_id: int = Query(gt=0), year: int = Query(gt=0)):
    return crud.get_customers_by_month_and_year(db, month_id, year)


@router.get("/get_customer_by_quarter", status_code=status.HTTP_200_OK)
async def get_customer_by_quarter(db: db_dependency, quarter: int = Query(gt=0), year: int = Query(gt=0)):
    return crud.get_customers_by_quarter_and_year(db, quarter, year)


@router.get("/get_customer_by_year", status_code=status.HTTP_200_OK)
async def get_customer_by_year(db: db_dependency, year: int = Query(gt=0)):
    return crud.get_customers_by_year(db, year)


@router.post("/create_customer", status_code=status.HTTP_201_CREATED)
async def create_customer(db: db_dependency, customer_request: CustomerRequest):
    return crud.create_customer(db, customer_request)


@router.put("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_customer(db: db_dependency, customer_request: CustomerRequest, customer_id: int = Path(gt=0)):
    return crud.update_customer(db, customer_id, customer_request)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(db: db_dependency, customer_id: int = Path(gt=0)):
    crud.delete_customer(db, customer_id)
