from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from models import Customer, Bill


def sum_total_bill(db: Session):
    customers = db.query(Customer).all()
    for customer in customers:
        customer_model = db.query(Customer).filter(Customer.id == customer.id).first()
        if customer_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')
        total_bill_amount = db.query(func.sum(Bill.amount)).filter(Bill.customer_id == customer.id).scalar()
        customer_model.total_bill = total_bill_amount or 0
        db.commit()


def set_customer_level(db: Session):
    customers = db.query(Customer).all()
    for customer in customers:
        customer_model = db.query(Customer).filter(Customer.id == customer.id).first()
        if customer_model is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')

        if customer_model.total_bill >= 500000:
            customer_model.level_id = 4
        elif customer_model.total_bill >= 200000:
            customer_model.level_id = 3
        elif customer_model.total_bill >= 100000:
            customer_model.level_id = 2
        else:
            customer_model.level_id = 1

        db.commit()
        db.refresh(customer_model)
