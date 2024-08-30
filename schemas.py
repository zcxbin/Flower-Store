from pydantic import BaseModel, Field


class CustomerRequest(BaseModel):
    name: str = Field(min_length=10)
    phone_number: str = Field(min_length=10)
    email: str = Field(min_length=10)
    gender: str = Field(min_length=1)

    class Config:
        from_attributes = True


class BillRequest(BaseModel):
    amount: int = Field(gt=0)
    customer_id: int = Field(gt=0)
    buying_date_id: int


class FlowerRequest(BaseModel):
    name: str = Field(min_length=0)
    description: str = Field(min_length=3, max_length=100)
    price: int = Field(gt=0)
    stock_quantity: int = Field(gt=0)
    category_id: int = Field(gt=0)

    class Config:
        from_attributes = True


