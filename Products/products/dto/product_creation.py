from marshmallow import Schema, fields, post_load
from werkzeug.datastructures import FileStorage

from products.models.product import Product


class ProductCreationSchema(Schema):
    title = fields.String(required=True, attribute='p_title', metadata={'description': 'Title of product'})
    description = fields.String(required=True, attribute='p_description',
                                metadata={'description': 'A short description'})
    price = fields.Integer(required=True, attribute='p_price', metadata={'description': 'Price'})
    address = fields.String(required=True, attribute='p_address', metadata={'description': 'Product Address'})
    category = fields.String(required=True, attribute='p_category', metadata={'description': 'Category of product'})
    status = fields.String(required=True, attribute='p_status', metadata={'description': 'Product Status'})
    titImage = fields.Field(metadata={'description': 'Primary Image', 'type': FileStorage})
    secImage = fields.Field(metadata={'description': 'Secondary Image', 'type': FileStorage})
    terImage = fields.Field(metadata={'description': 'Tertiary Image', 'type': FileStorage})

    @post_load
    def add_product(self, data, **kwargs):
        return Product(**data)
