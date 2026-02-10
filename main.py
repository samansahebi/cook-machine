from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from controllers.conveyors import Conveyors
from controllers.pos import POSRequest
from models import models
from models import schemas
from models.database import engine, SessionLocal
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqladmin import Admin
from models.admin import ProductAdmin, TransactionAdmin
from fastapi.staticfiles import StaticFiles


models.Base.metadata.create_all(bind=engine)
app = FastAPI()
admin = Admin(app, engine)
admin.add_view(ProductAdmin)
admin.add_view(TransactionAdmin)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
def products_page(
    request: Request,
    db: Session = Depends(get_db)
):
    products = db.query(models.Product).all()
    return templates.TemplateResponse(
        "products.html",
        {"request": request, "products": products}
    )


@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return products


@app.post("/buy")
def buy_product(item: schemas.BuyProduct, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == item.id).first()
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

        return JSONResponse({"result": "success"}, 200)

    return JSONResponse({"error": "failed"}, 400)


@app.post("/add-product", response_model=schemas.ProductResponse)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = models.Product(**product.dict())

    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product


@app.post("/update-product/{product_id}", response_model=schemas.ProductResponse)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update only provided fields
    update_data = product.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_product, field, value)

    db.commit()
    db.refresh(db_product)
    return db_product

