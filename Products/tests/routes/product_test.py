import io
import json
from unittest import mock
from unittest.mock import patch, MagicMock

import pytest
from flask import url_for
from products.extensions import db
from products.models.product import Product
from products.models.product_category import ProductCategory
from products.models.product_images import ProductImage
from products.models.product_status import ProductStatus
from products.routes.product import update_product, get_my_products
from tests import conf_test


@pytest.fixture(scope='module')
def product_category():
    with url_for('products').app_context():
        new_category = ProductCategory(pc_name='TestCategory')
        db.session.add(new_category)
        db.session.commit()
        yield new_category
        db.session.delete(new_category)
        db.session.commit()


@pytest.fixture(scope='module')
def product_status():
    with url_for('products').app_context():
        new_status = ProductStatus(ps_name='TestStatus')
        db.session.add(new_status)
        db.session.commit()
        yield new_status
        db.session.delete(new_status)
        db.session.commit()


def test_get_all_products_with_token(flask_app):
    # Mock the test client
    client = MagicMock()
    client.post.return_value = "Mocked response"

    # create some test products
    product_status = ProductStatus(ps_name="test status")
    product_category = ProductCategory(pc_name="test category")
    product_1 = Product(p_title="Test Product 1", p_description="Test Description 1", p_price=10.99,
                        p_address="Test Address 1", p_status=product_status.ps_id, p_category=product_category.pc_id,
                        p_userId=1)
    product_2 = Product(p_title="Test Product 2", p_description="Test Description 2", p_price=20.99,
                        p_address="Test Address 2", p_status=product_status.ps_id, p_category=product_category.pc_id,
                        p_userId=2)

    # Mock the database interactions
    with patch('products.models.product_status') as mock_product_status, \
            patch('products.models.product_category') as mock_product_category, \
            patch('products.models.product') as mock_product:
        mock_product_status.return_value = product_status
        mock_product_category.return_value = product_category
        mock_product.query.filter.return_value.all.return_value = [product_1, product_2]

        response = flask_app.get(url_for("products.get_all_products"))
        assert response.status_code == 200

        # check if the expected data is returned
        expected_data = [
            {
                "id": product_1.p_id,
                "title": "Test Product 1",
                "description": "Test Description 1",
                "price": 10.99,
                "address": "Test Address 1",
                "status": "test status",
                "category": "test category",
                "user_id": 1
            },
            {
                "id": product_2.p_id,
                "title": "Test Product 2",
                "description": "Test Description 2",
                "price": 20.99,
                "address": "Test Address 2",
                "status": "test status",
                "category": "test category",
                "user_id": 2
            }
        ]
        assert json.loads(response.data) == expected_data


def test_get_all_products_without_token(flask_app):
    # call the endpoint without token
    response = flask_app.get('/getProducts')
    assert response.status_code == 401


@pytest.fixture
def product_data():
    return {
        'p_title': 'Test Product',
        'p_description': 'This is a test product.',
        'p_price': 10.0,
        'p_address': '123 Test St',
        'p_category': 'Electronics',
        'p_status': 'Available',
        'titImage': (io.BytesIO(b'test image'), 'test.jpg'),
        'secImage': (io.BytesIO(b'test image'), 'test.jpg'),
        'terImage': (io.BytesIO(b'test image'), 'test.jpg'),
    }


@patch('products.routes.product.add_product_images')
def test_create_product_success(add_product_images_mock, client, product_data):
    add_product_images_mock.return_value = True

    response = conf_test.client.post('/createProduct', data=product_data)
    assert response.status_code == 204
    assert response.json == {'message': 'Product created successfully'}


@patch('products.routes.product.add_product_images')
def test_create_product_validation_error(add_product_images_mock, client):
    response = client.post('/createProduct', data={})
    assert response.status_code == 400
    assert response.json == {'Error': {'p_title': ['Missing data for required field.'],
                                       'p_description': ['Missing data for required field.'],
                                       'p_price': ['Missing data for required field.'],
                                       'p_address': ['Missing data for required field.'],
                                       'p_category': ['Missing data for required field.'],
                                       'p_status': ['Missing data for required field.']}}


@mock.patch('products.routes.product.add_product_images')
def test_create_product_database_error(add_product_images_mock, client, product_data):
    add_product_images_mock.return_value = False

    response = client.post('/createProduct', data=product_data)
    assert response.status_code == 500
    assert response.json == {'message': 'An error occurred while adding product'}


@patch('products.routes.product.add_product_images')
def test_create_product_token_decoding_error(add_product_images_mock, client, product_data):
    with patch('app.routes.products.decode_token', side_effect=Exception('Test Error')):
        response = client.post('/createProduct', data=product_data)
        assert response.status_code == 401
        assert response.json == {'message': 'Token decoding error'}


@patch('products.routes.product.add_product_images')
def test_create_product_invalid_category_or_status_error(add_product_images_mock, client, product_data):
    with patch('app.routes.products.db.session.query') as query_mock:
        query_mock.filter_by.return_value.first.return_value = None

        response = client.post('/createProduct', data=product_data)
        assert response.status_code == 400
        assert response.json == {'Error': 'Invalid category or status'}


@pytest.fixture(scope='module')
def new_product_image():
    product_image = ProductImage(
        pi_productId=1,
        pi_primImage=b'',
        pi_secImage=b'',
        pi_terImage=b''
    )
    return product_image


def test_add_product_images(db_session, new_product_image):
    # Add the product image to the database
    db_session.add(new_product_image)
    db_session.commit()

    # Retrieve the product image from the database
    product_image = db_session.query(ProductImage).filter_by(pi_id=new_product_image.pi_id).first()

    # Check that the product image was added successfully
    assert product_image is not None
    assert product_image.pi_productId == 1
    assert product_image.pi_primImage == b''
    assert product_image.pi_secImage == b''
    assert product_image.pi_terImage == b''


def test_add_product_images_error(db_session):
    # Try to add a product image with missing fields
    product_image = ProductImage(pi_productId=1)
    db_session.add(product_image)
    with pytest.raises(Exception):
        db_session.commit()


def test_get_product_image_success(client, db_session, new_product, new_product_image):
    # create a product with an image
    new_product.p_titImage = b'test image'
    db_session.add(new_product)
    db_session.commit()

    # create the corresponding product image
    new_product_image.pi_productId = new_product.p_id
    new_product_image.pi_primImage = b'test image'
    db_session.add(new_product_image)
    db_session.commit()

    # make a request to the endpoint
    response = client.get(f'/products/getProductImage/{new_product.p_id}')

    # check that the response status code is 200
    assert response.status_code == 200

    # check that the response contains the correct product_id and image data
    expected_response_data = {
        "product_id": new_product.p_id,
        "pi_primImage": "dGVzdCBpbWFnZQ=="
    }
    assert response.json == expected_response_data


def test_get_product_image_not_found(client, db_session):
    # make a request for a non-existent product id
    response = client.get('/products/getProductImage/999')

    # check that the response status code is 404 and the message is correct
    assert response.status_code == 404
    assert response.json == {'message': 'Product images not found'}


def test_get_product_image_encoding_error(client, db_session, new_product, new_product_image):
    # create a product with an image that cannot be encoded
    new_product.p_titImage = b'test image'
    db_session.add(new_product)
    db_session.commit()

    # create the corresponding product image
    new_product_image.pi_productId = new_product.p_id
    new_product_image.pi_primImage = b'test image'
    db_session.add(new_product_image)
    db_session.commit()

    # patch the base64.b64encode function to raise an error
    with patch('base64.b64encode') as mock_b64encode:
        mock_b64encode.side_effect = Exception('encoding error')

        # make a request to the endpoint
        response = client.get(f'/products/getProductImage/{new_product.p_id}')

    # check that the response status code is 200
    assert response.status_code == 200

    # check that the response contains the correct product_id and message
    assert response.json == {'product_id': new_product.p_id}


def test_update_product_success(client, mocker):
    mock_request = mocker.patch('flask.request')
    mock_request.get_json.return_value = {"product_id": 1, "status": "available"}
    mock_db_session = mocker.patch('app.db.session')
    mock_query = mock_db_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = {"p_id": 1}
    mock_product_status = mock_query.filter_by.return_value.first.return_value = {"ps_name": "available"}

    response = update_product()

    assert response.status_code == 200
    assert json.loads(response.get_data(as_text=True)) == {'message': 'Product updated successfully'}


def test_update_product_invalid_product_id(client, mocker):
    mock_request = mocker.patch('flask.request')
    mock_request.get_json.return_value = {"product_id": 999, "status": "available"}
    mock_db_session = mocker.patch('app.db.session')
    mock_query = mock_db_session.query.return_value
    mock_query.filter_by.return_value.first.return_value = None

    response = update_product()

    assert response.status_code == 404
    assert json.loads(response.get_data(as_text=True)) == {'message': 'Product not found'}


def test_delete_product(client):
    # create a product to be deleted
    product = {
        "p_title": "Test Product",
        "p_description": "This is a test product",
        "p_price": 99.99,
        "p_address": "123 Test Street",
        "p_category": "Test Category",
        "p_userId": 1
    }
    response = client.post('/product', data=product, content_type='multipart/form-data')
    assert response.status_code == 204

    # delete the product
    response = client.delete('/product/1')
    assert response.status_code == 200
    assert json.loads(response.data) == {'message': 'Product deleted successfully'}

    # check that the product has been deleted from the database
    response = client.get('/product/1')
    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'Product not found'}


def test_delete_product_not_found(client):
    # delete a product that doesn't exist
    response = client.delete('/product/1')
    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'invalid product'}


def test_delete_product_wrong_user(client):
    # create a product owned by user 1
    product = {
        "p_title": "Test Product",
        "p_description": "This is a test product",
        "p_price": 99.99,
        "p_address": "123 Test Street",
        "p_category": "Test Category",
        "p_userId": 1
    }
    response = client.post('/product', data=product, content_type='multipart/form-data')
    assert response.status_code == 204

    # delete the product as user 2
    with client.session_transaction() as session:
        session['token'] = {'username': 2}
    response = client.delete('/product/1')
    assert response.status_code == 404
    assert json.loads(response.data) == {'message': 'invalid product'}


def test_delete_images(flask_app):
    # set up test data and login user
    product_id = 1
    # mock the delete_images function
    with mock.patch('products.routes.products.delete_images') as mocked_delete_images:
        mocked_delete_images.return_value = True

        # send delete product request
        response = flask_app.delete(f'/products/{product_id}')
        data = response.get_json()

        # check that the response and data are as expected
        assert response.status_code == 200
        assert data['message'] == 'Product deleted successfully'

        # check that the mocked function was called with the correct arguments
        mocked_delete_images.assert_called_once_with(product_id)


def test_get_my_products_success(flask_app):
    with flask_app.test_request_context():
        with patch('products.db.session.query') as mock_query:
            # Mock the query results
            mock_query.return_value.join.return_value.join.return_value \
                .filter.return_value.add_columns.return_value.all.return_value = [
                (1, 'Product 1', 'Description 1', 10.0, 'Address 1', 'Status 1', 'Category 1', 1, b'Binary Image 1'),
                (2, 'Product 2', 'Description 2', 20.0, 'Address 2', 'Status 2', 'Category 2', 1, b'Binary Image 2')
            ]

            # Mock the decoded token
            decoded_token = {'userId': 1}

            # Call the method
            response = get_my_products(decoded_token=decoded_token)

            # Check the response
            assert response.status_code == 200
            assert len(json.loads(response.get_data())) == 2


def test_get_my_products_no_products():
    with patch('products.db.session.query') as mock_query:
        # Mock the query result to return an empty list
        mock_query.return_value.join.return_value.join.return_value \
            .filter.return_value.add_columns.return_value.all.return_value = []

        # Mock the decoded token
        decoded_token = {'userId': 1}

        # Call the method
        response = get_my_products(decoded_token=decoded_token)

        # Check the response
        assert response.status_code == 200
        assert len(json.loads(response.get_data())) == 0


def test_get_my_products_database_error():
    with patch('products.db.session.query') as mock_query:
        # Mock the query to raise an exception
        mock_query.side_effect = Exception('Database error')

        # Mock the decoded token
        decoded_token = {'userId': 1}

        # Call the method
        response = get_my_products(decoded_token=decoded_token)

        # Check the response
        assert response.status_code == 500
