from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status
from sqlalchemy.exc import IntegrityError
from models import Customer, Bill, Revenue


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


def calculate_and_save_revenue(db: Session):
    # Tính tổng doanh thu từ bảng 'Bill'
    total_revenue = db.query(func.sum(Bill.amount)).scalar() or 0

    # Tạo một bản ghi mới trong bảng 'Revenue' với tổng doanh thu
    revenue_record = Revenue(total_revenue=total_revenue)
    db.add(revenue_record)

    try:
        db.commit()
        db.refresh(revenue_record)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error saving revenue")
