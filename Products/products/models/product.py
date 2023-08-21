from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from products.models import product_table_name
from products.extensions import db
from products.models.product_category import ProductCategory
from products.models.product_status import ProductStatus


class Product(db.Model):
    __tablename__ = product_table_name

    p_id = db.Column(BigInteger, primary_key=True)
    p_title = db.Column(db.String(100), nullable=False)
    p_description = db.Column(db.String(200), nullable=False)
    p_price = db.Column(db.Integer, nullable=False)
    p_address = db.Column(db.String(100))
    p_category = db.Column(db.Integer, db.ForeignKey(ProductCategory.pc_id))
    p_userId = db.Column(db.Integer, nullable=False)
    p_status = db.Column(db.Integer, db.ForeignKey(ProductStatus.ps_id), default=1)
    p_titImage = db.Column(db.LargeBinary(length=4 * 1024 * 1024))  # to store image size up to 4MB
    category = relationship(ProductCategory.__name__)
    status = relationship(ProductStatus.__name__)


class ProductSchema(SQLAlchemyAutoSchema):
    p_id = auto_field()
    p_title = auto_field()
    p_description = auto_field()
    p_price = auto_field()
    p_address = auto_field()
    p_category = auto_field()
    p_userId = auto_field()
    p_status = auto_field()
    p_titImage = auto_field()

    class Meta:
        model = Product
        include_relationships = True
        load_instance = True
