from products import db
from products.models import product_category_table_name


class ProductCategory(db.Model):
    __tablename__ = product_category_table_name

    pc_id = db.Column(db.Integer, primary_key=True)
    pc_name = db.Column(db.String(45), nullable=False)