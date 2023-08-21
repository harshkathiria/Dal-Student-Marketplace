from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger

from products import db
from products.models import product_image_table_name
from products.models.product import Product


class ProductImage(db.Model):
    __tablename__ = product_image_table_name
    pi_productId = db.Column(db.Integer, db.ForeignKey(Product.p_id))
    pi_primImage = db.Column(db.LargeBinary(length=4 * 1024 * 1024))
    pi_secImage = db.Column(db.LargeBinary(length=4 * 1024 * 1024))
    pi_terImage = db.Column(db.LargeBinary(length=4 * 1024 * 1024))
    pi_id = db.Column(BigInteger, primary_key=True)

    product = relationship(Product.__name__)


class ProductImageSchema(SQLAlchemyAutoSchema):
    pi_productId = auto_field()
    pi_primImage = auto_field()
    pi_secImage = auto_field()
    pi_terImage = auto_field()
    pi_id = auto_field()

    class Meta:
        model = ProductImage
        include_relationships = True
        load_instance = True
