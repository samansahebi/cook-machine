from sqladmin import Admin, ModelView
from .models import Product, Transaction
from sqladmin.fields import FileField


class ProductAdmin(ModelView, model=Product):
    column_list = [
        Product.id,
        Product.name,
        Product.price,
        Product.quantity,
        Product.floor_id,
    ]

    form_overrides = {
        "cover_image": FileField
    }

    form_args = {
        "cover_image": {
            "label": "Cover Image",
            "base_path": "static/uploads/products",
            "allow_overwrite": False,
        }
    }

    column_searchable_list = [Product.name]
    column_sortable_list = [Product.id, Product.price]


class TransactionAdmin(ModelView, model=Transaction):
    column_list = [
        Transaction.product_id,
        Transaction.id,
        Transaction.amount,
        Transaction.trace,
        Transaction.pan,
        Transaction.rrn,
        Transaction.data1,
        Transaction.created_at,
    ]
    column_searchable_list = [Transaction.trace]
    column_sortable_list = [Transaction.id, Transaction.amount]
