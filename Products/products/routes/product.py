import base64
import json
from distutils.file_util import write_file

from flask import jsonify, request, Blueprint, Response
from sqlalchemy import update, delete
from werkzeug.routing import ValidationError

from products.dto.product_change import ProductUpdateSchema
from products.extensions import db
from products.dto.product_creation import ProductCreationSchema
from products.models.product_category import ProductCategory
from products.models.product_images import ProductImage
from products.models.product_status import ProductStatus
from products.models.product import Product
from products.routes import authenticate_token
from sqlalchemy import and_

products_bp = Blueprint("products", __name__, url_prefix="/products")
product_schema = ProductCreationSchema
product_update = ProductUpdateSchema


@products_bp.route("/getProducts", methods=["GET"])
@authenticate_token
def get_all_products(*args, **kwargs):
    products = db.session.query(Product).join(ProductStatus, Product.p_status == ProductStatus.ps_id) \
        .join(ProductCategory, Product.p_category == ProductCategory.pc_id) \
        .filter(and_(Product.p_status == 1)) \
        .add_columns(Product.p_id, Product.p_title, Product.p_description, Product.p_price,
                     Product.p_address, ProductStatus.ps_name, ProductCategory.pc_name, Product.p_userId,
                     Product.p_titImage).all()
    product_list = []

    for product in products:
        product_dict = {
            "id": product.p_id,
            "title": product.p_title,
            "description": product.p_description,
            "price": product.p_price,
            "address": product.p_address,
            "status": product.ps_name,
            "category": product.pc_name,
            "user_id": product.p_userId
        }

        # decode product image binary to base64 string
        if product.p_titImage:
            image_data = base64.b64encode(product.p_titImage).decode('utf-8')
            product_dict["titImage"] = image_data

        product_list.append(product_dict)
    return jsonify(product_list), 200


@products_bp.route("/addProduct", methods=["POST"])
@authenticate_token
def create_product(*args, **kwargs):
    try:
        product_data = product_schema().load(request.form)
        product_data.titImage = request.files.get('titImage')
        product_data.secImage = request.files.get('secImage')
        product_data.terImage = request.files.get('terImage')
    except ValidationError as err:
        return jsonify({'Error': err.messages}), 400

    product_status = db.session.query(ProductStatus).filter_by(ps_name=product_data.p_status).first()
    product_category = db.session.query(ProductCategory).filter_by(pc_name=product_data.p_category).first()
    decoded_token = kwargs.get('decoded_token')
    user_id = decoded_token['user_id']
    thumbnail = product_data.titImage
    new_product = Product(
        p_title=product_data.p_title,
        p_description=product_data.p_description,
        p_price=product_data.p_price,
        p_address=product_data.p_address,
        p_category=product_category.pc_id,
        p_userId=user_id,
        p_status=product_status.ps_id,
        p_titImage=thumbnail.read()
    )
    db.session.add(new_product)
    db.session.commit()

    product_id = new_product.p_id
    # Update file pointer to start of file
    product_data.titImage.seek(0)
    add_images = add_product_images(product_data, product_id)
    if add_images:
        return jsonify({'message': 'Product created successfully'}), 204
    else:
        return jsonify({'message': 'An error occurred while adding product'}), 500


def add_product_images(product_data, product_id):
    product_images = ProductImage(
        pi_productId=product_id,
        pi_primImage=product_data.titImage.read(),
        pi_secImage=product_data.secImage.read(),
        pi_terImage=product_data.terImage.read()
    )
    db.session.add(product_images)
    db.session.commit()

    if product_images.pi_id:
        return True
    else:
        return False


@products_bp.route("/getProduct/readImages/<int:product_id>", methods=["GET"])
@authenticate_token
def get_product_image(product_id, **kwargs):
    product_images = db.session.query(ProductImage).filter_by(pi_productId=product_id).first()
    if not product_images:
        return jsonify({'message': 'Product images not found'}), 404

    product_image_dict = {"product_id": product_images.pi_productId}
    image_fields = ["pi_primImage", "pi_secImage", "pi_terImage"]
    for field in image_fields:
        try:
            image_data = getattr(product_images, field)
            if image_data:
                # write_file(image_data, "/Users/ashutoshsagar/Documents/image.png")
                image_data = base64.b64encode(image_data).decode('utf-8')
                # write_file(image_data, "/Users/ashutoshsagar/Documents/image.txt")
                product_image_dict[field] = image_data
        except Exception as e:
            print(f'error encoding {field}: {e}')

    response = Response(json.dumps(product_image_dict), status=200)
    response.headers['Content-Type'] = 'application/json'
    return response


@products_bp.route("/updateProduct", methods=["POST"])
@authenticate_token
def update_product(*args, **kwargs):
    req_data = request.get_json()
    update_req = ProductUpdateSchema.load(data=req_data)

    product_status = db.session.query(ProductStatus).filter_by(ps_name=update_req.status).first()
    # Check for valid product entry in database
    product = db.session.query(Product).filter_by(p_id=update_req.product_id).first()
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    else:
        db.session.execute((update(Product).
                            where(Product.p_id == update_req.product_id).
                            values(p_status=product_status.ps_id)))
        db.session.commit()

        return jsonify({'message': 'Product updated successfully'}), 200


@products_bp.route("/deleteProduct/<int:product_id>", methods=["POST"])
@authenticate_token
def delete_product(product_id, **kwargs):
    decoded_token = kwargs.get('decoded_token')
    user_id = decoded_token['user_id']

    # request_data = request.get_json()
    # fetch the product from database and validate if the product exists and is from same user
    product = db.session.query(Product).filter_by(p_id=product_id).first()
    if not product and product.p_userId == user_id:
        return jsonify({'message': 'invalid product'}), 404

    # fetch status code for Deleted product
    product_status = db.session.query(ProductStatus).filter_by(ps_name='Deleted').first()

    db.session.execute((update(Product).
                        where(Product.p_id == product_id).
                        values(p_status=product_status.ps_id)))
    db.session.commit()
    # delete images in db
    delete_images(product_id)
    return jsonify({'message': 'Product deleted successfully'}), 200


def delete_images(product_id):
    try:
        db.session.execute((delete(ProductImage).where(ProductImage.pi_productId == product_id)))
        db.session.commit()
    except Exception as e:
        print(e)
        print(f'error in deleting images for product {product_id}')


@products_bp.route("/myProducts", methods=["GET"])
@authenticate_token
def get_my_products(*args, **kwargs):
    decoded_token = kwargs.get('decoded_token')
    user_id = decoded_token['user_id']

    products = db.session.query(Product).join(ProductStatus, Product.p_status == ProductStatus.ps_id) \
        .join(ProductCategory, Product.p_category == ProductCategory.pc_id) \
        .filter(Product.p_userId == user_id) \
        .add_columns(Product.p_id, Product.p_title, Product.p_description, Product.p_price,
                     Product.p_address, ProductStatus.ps_name, ProductCategory.pc_name, Product.p_userId,
                     Product.p_titImage).all()
    product_list = []

    for product in products:
        product_dict = {
            "id": product.p_id,
            "title": product.p_title,
            "description": product.p_description,
            "price": product.p_price,
            "address": product.p_address,
            "status": product.ps_name,
            "category": product.pc_name,
            "user_id": product.p_userId
        }

        # decode product image binary to base64 string
        if product.p_titImage:
            image_data = base64.b64encode(product.p_titImage).decode('utf-8')
            product_dict["titImage"] = image_data

        product_list.append(product_dict)
    return jsonify(product_list), 200




