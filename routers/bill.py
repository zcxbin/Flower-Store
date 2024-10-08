from fastapi import APIRouter, Path, status, Query
from dependency import db_dependency
import crud
from modify import sum_total_bill, set_customer_level
from schemas import BillRequest

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
async def get_bills(db: db_dependency):
    return crud.get_bills(db)


@router.post("/create_bill", status_code=status.HTTP_201_CREATED)
async def create_bill(db: db_dependency, bill_request: BillRequest):
    sum_total_bill(db)
    set_customer_level(db)
    return crud.create_bill(db, bill_request)


@router.put("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_bill(db: db_dependency, bill_request: BillRequest, bill_id: int = Path(gt=0)):
    return crud.update_bill(db, bill_id, bill_request)


@router.delete("/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bill(db: db_dependency, bill_id: int = Path(gt=0)):
    crud.delete_bill(db, bill_id)
