from products import db
from products.models import product_status_table_name


class ProductStatus(db.Model):
    __tablename__ = product_status_table_name

    ps_id = db.Column(db.Integer, primary_key=True)
    ps_name = db.Column(db.String(45), nullable=False)