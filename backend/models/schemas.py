from pydantic import BaseModel


class BuyProduct(BaseModel):
    id: int

class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    cover: str | None = None
    price: int
    quantity: int
    stepper_id: int
    step_count: int
    floor_id: int

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    cover: str | None = None
    price: int | None = None
    quantity: int | None = None
    stepper_id: int | None = None
    step_count: int | None = None
    floor_id: int | None = None

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True
