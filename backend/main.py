from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.responses import Response

from backend.controllers.conveyors import Conveyors
from backend.controllers.pos import POSRequest
from models import models
from models import schemas
from models.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return Response(products, 200)


@app.post("/buy")
def buy_product(item: schemas.BuyProduct, db: Session = Depends(get_db)):
    product = models.Product(id=item.id)
    pos = POSRequest()
    res = pos.send_request(product.price)
    if res.get("resp") == 0:
        db_item = models.Transaction(
            product_id=product.id,
            amount=res.get("amount"),
            status="success",
            pan=res.get("pan"),
            rrn=res.get("rrn"),
            trace=res.get("trace"),
            data1=res.get("data1"),
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        conveyor = Conveyors()
        conveyor.move_elevator(product.floor_id)
        conveyor.deliver_product(product.floor_id,
                                 product.stepper_id,
                                 product.step_count,
                                 delay_us=800)
        conveyor.move_elevator("exit")
        conveyor.move_elevators_conveyor()
        conveyor.move_elevator("start")

        return Response({"result": "success"}, 200)

    return Response({"error": "failed"}, 400)


@app.post("/add-product")
def add_product(db: Session = Depends(get_db)):
    product = models.Product()
    return Response(product, 201)


@app.post("/update-product")
def update_product(db: Session = Depends(get_db)):
    product = models.Product()
    return Response(product, 200)