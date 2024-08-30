from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Bill(Base):
    __tablename__ = 'bill'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    buying_date_id = Column(Integer, ForeignKey('buying_date.id'))

    customer = relationship('Customer', back_populates='bills')
    buying_date = relationship('BuyingDate', back_populates='bills')


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)

    flowers = relationship('Flower', back_populates='category')


class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone_number = Column(String)
    email = Column(String)
    gender = Column(String)
    level_id = Column(Integer, ForeignKey('level.id'))
    total_bill = Column(Integer, default=0)

    bills = relationship('Bill', back_populates='customer')
    level = relationship('Level', back_populates='customers')

    # Quan hệ nhiều-nhiều với bảng BuyingDate thông qua bảng trung gian Customer_BuyingDate
    buying_dates = relationship('Customer_BuyingDate', back_populates='customer')


class BuyingDate(Base):
    __tablename__ = 'buying_date'
    id = Column(Integer, primary_key=True, index=True)
    YYYYMMDD = Column(Integer)

    bills = relationship('Bill', back_populates='buying_date')

    # Quan hệ nhiều-nhiều với Customer thông qua bảng trung gian Customer_BuyingDate
    customers = relationship('Customer_BuyingDate', back_populates='buying_date')


class Customer_BuyingDate(Base):
    __tablename__ = 'customer_buying_date'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    buying_date_id = Column(Integer, ForeignKey('buying_date.id'))

    # Thiết lập quan hệ ngược về bảng Customer và BuyingDate
    customer = relationship('Customer', back_populates='buying_dates')
    buying_date = relationship('BuyingDate', back_populates='customers')


class Date(Base):
    __tablename__ = 'date'
    id = Column(Integer, primary_key=True, index=True)
    day = Column(Integer)
    month = Column(Integer)
    year = Column(Integer)
    Buying_date_id = Column(Integer, ForeignKey('buying_date.id'))
    Leap_year = Column(Boolean)

    revenue = relationship('Revenue', back_populates='date')


class Flower(Base):
    __tablename__ = 'flower'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    stock_quantity = Column(Integer)
    category_id = Column(Integer, ForeignKey('category.id'))

    category = relationship('Category', back_populates='flowers')


class Level(Base):
    __tablename__ = 'level'
    id = Column(Integer, primary_key=True, index=True)
    level_name = Column(String)

    customers = relationship('Customer', back_populates='level')


class Revenue(Base):
    __tablename__ = 'revenue'
    id = Column(Integer, primary_key=True, index=True)
    date_id = Column(Integer, ForeignKey('date.id'))
    amount = Column(Integer)

    date = relationship('Date', back_populates='revenue')
