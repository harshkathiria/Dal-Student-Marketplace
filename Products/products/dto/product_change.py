from marshmallow import Schema, fields, post_load


class ProductUpdate:
    def __init__(self, product_id, status):
        self.product_id = product_id
        self.status = status


class ProductUpdateSchema(Schema):
    product_id = fields.Integer(required=True, metadata={'description': 'Product Id'})
    status = fields.String(required=True, metadata={'description': 'Product Status'})

    @post_load
    def update_product(self, data, **kwargs):
        return ProductUpdate(**data)

