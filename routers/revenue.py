from fastapi import APIRouter, Path, status, Query
from dependency import db_dependency
import crud
from schemas import CustomerRequest
from modify import sum_total_bill, set_customer_level

router = APIRouter()


@router.get('/read_revenue_by_day')
async def read_revenue_by_day(db: db_dependency, day: int = Query(gt=0), month: int = Query(gt=0), year: int = Query(gt=0)):
    return crud.get_revenue_by_day(db, day, month, year)


@router.get('/read_revenue_by_month')
async def read_revenue_by_month(db: db_dependency, month: int = Query(gt=0), year: int = Query(gt=0)):
    return crud.get_revenue_by_month(db, month, year)


@router.get('/read_revenue_by_quarter')
async def read_revenue_by_quarter(db: db_dependency, quarter: int = Query(gt=0), year: int = Query(gt=0)):
    return crud.get_revenue_by_quarter(db, quarter, year)


@router.get('/read_revenue_by_year')
async def read_revenue_by_year(db: db_dependency, year: int = Query(gt=0)):
    return crud.get_revenue_by_year(db, year)
