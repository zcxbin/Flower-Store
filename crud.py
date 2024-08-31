from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import Customer, Bill, Flower, Customer_BuyingDate, BuyingDate
from sqlalchemy import and_, func


def create_customer(db: Session, customer_request):
    customer_model = Customer(**customer_request.model_dump())
    db.add(customer_model)
    db.commit()
    db.refresh(customer_model)
    return customer_model


def get_customers(db: Session):
    return db.query(Customer).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(Customer).filter(Customer.id == customer_id).first()


def update_customer(db: Session, customer_id: int, customer_request):
    customer_model = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')

    customer_model.name = customer_request.name
    customer_model.level_id = customer_request.level_id
    db.commit()
    db.refresh(customer_model)
    return customer_model


def delete_customer(db: Session, customer_id: int):
    customer_model = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Customer not found')

    db.delete(customer_model)
    db.commit()


def create_bill(db: Session, bill_request):
    bill_model = Bill(**bill_request.model_dump())
    db.add(bill_model)
    db.commit()
    db.refresh(bill_model)
    return bill_model


def get_bills(db: Session):
    return db.query(Bill).all()


def update_bill(db: Session, bill_id: int, bill_request):
    bill_model = db.query(Bill).filter(Bill.id == bill_id).first()
    if bill_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bill not found')

    bill_model.amount = bill_request.amount
    db.commit()
    db.refresh(bill_model)
    return bill_model


def delete_bill(db: Session, bill_id: int):
    bill_model = db.query(Bill).filter(Bill.id == bill_id).first()
    if bill_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Bill not found')

    db.delete(bill_model)
    db.commit()


def create_flower(db: Session, flower_request):
    flower_model = Flower(**flower_request.model_dump())
    db.add(flower_model)
    db.commit()
    db.refresh(flower_model)
    return flower_model


def get_flowers(db: Session):
    return db.query(Flower).all()


def get_flower_by_id(db: Session, flower_id: int):
    return db.query(Flower).filter(flower_id == Flower.id).first()


def update_flower(db: Session, flower_id: int, flower_request):
    flower_model = db.query(Flower).filter(flower_id == Flower.id).first()
    if flower_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Flower not found')
    flower_model.name = flower_request.name
    flower_model.description = flower_request.description
    flower_model.price = flower_request.price
    flower_model.stock_quantity = flower_request.stock_quanity
    flower_model.category = flower_request.category

    db.commit()
    db.refresh(flower_model)
    return flower_model


def delete_flower(db: Session, flower_id: int):
    flower_model = db.query(Flower).filter(flower_id == Flower.id).first()
    if flower_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Flower not found')
    db.delete(flower_model)
    db.commit()


def get_customer_by_level(db: Session, level_id: int):
    return db.query(Customer).filter(Customer.level_id == level_id).all()


def get_customers_by_month_and_year(db: Session, month: int, year: int):
    customers = db.query(Customer).join(Customer_BuyingDate).join(BuyingDate).filter(
        and_(
            (BuyingDate.YYYYMMDD // 10000 == year),
            ((BuyingDate.YYYYMMDD % 10000) // 100 == month)
        )
    ).all()
    return customers


def get_customers_by_quarter_and_year(db: Session, quarter: int, year: int):
    month_ranges = {
        1: (1, 3),
        2: (4, 6),
        3: (7, 9),
        4: (10, 12)
    }
    start_month, end_month = month_ranges.get(quarter, (1, 12))

    customers = db.query(Customer).join(Customer_BuyingDate).join(BuyingDate).filter(
        and_(
            (BuyingDate.YYYYMMDD // 10000 == year),
            (BuyingDate.YYYYMMDD % 10000 // 100 >= start_month),
            (BuyingDate.YYYYMMDD % 10000 // 100 <= end_month)
        )
    ).all()
    return customers


def get_customers_by_year(db: Session, year: int):
    customers = db.query(Customer).join(Customer_BuyingDate).join(BuyingDate).filter(
        and_
        (BuyingDate.YYYYMMDD // 10000 == year)
    ).all()
    return customers


def get_revenue_by_day(db: Session, day: int, month: int, year: int):
    revenue = db.query(func.sum(Bill.amount)).join(BuyingDate).filter(
        and_(
            (BuyingDate.YYYYMMDD // 10000 == year),
            (BuyingDate.YYYYMMDD % 10000 // 100 == month),
            (BuyingDate.YYYYMMDD % 100 == day)
        )
    ).scalar()

    if revenue is None or revenue == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Revenue not found')

    return f'revenue {day}/{month}/{year} is {revenue}'


def get_revenue_by_month(db: Session, month: int, year: int):
    revenue = db.query(func.sum(Bill.amount)).join(BuyingDate).filter(
        and_(
            (BuyingDate.YYYYMMDD // 10000 == year),
            (BuyingDate.YYYYMMDD % 10000 // 100 == month)
        )
    ).scalar()
    if revenue is None or revenue == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Revenue not found')
    return f'revenue {month}/{year} is {revenue}'


def get_revenue_by_quarter(db: Session, quarter: int, year: int):
    month_ranges = {
        1: (1, 3),
        2: (4, 6),
        3: (7, 9),
        4: (10, 12)
    }
    start_month, end_month = month_ranges.get(quarter, (1, 12))

    revenue = db.query(func.sum(Bill.amount)).join(BuyingDate).filter(
        and_(
            (BuyingDate.YYYYMMDD // 10000 == year),
            (BuyingDate.YYYYMMDD % 10000 // 100 >= start_month),
            (BuyingDate.YYYYMMDD % 10000 // 100 <= end_month)
        )
    ).scalar()
    if revenue is None or revenue == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Revenue not found')
    return f'revenue {quarter} of {year} is {revenue}'



def get_revenue_by_year(db: Session, year: int):
    revenue = db.query(func.sum(Bill.amount)).join(BuyingDate).filter(
        and_
        (BuyingDate.YYYYMMDD // 10000 == year)
    ).scalar()
    if revenue is None or revenue == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Revenue not found')
    return f'revenue {year} is {revenue}'
