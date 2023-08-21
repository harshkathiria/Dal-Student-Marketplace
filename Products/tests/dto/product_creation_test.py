import io

import pytest
from marshmallow import ValidationError, EXCLUDE
from werkzeug.datastructures import FileStorage

from products.dto.product_creation import ProductCreationSchema


def test_valid_product_creation_schema():
    # Arrange
    valid_data = {
        'title': 'Test product',
        'description': 'This is a test product',
        'price': 100,
        'address': '123 Test St',
        'category': 'Test category',
        'status': 'Available',
    }
    # Act
    result = ProductCreationSchema().load(valid_data)
    # Assert
    assert result.p_title == valid_data['title']
    assert result.p_description == valid_data['description']
    assert result.p_price == valid_data['price']
    assert result.p_address == valid_data['address']
    assert result.p_category == valid_data['category']
    assert result.p_status == valid_data['status']


def test_invalid_product_creation_schema():
    # Arrange
    invalid_data = {
        'title': 'Test product',
        'description': 'This is a test product',
        'price': 'invalid_price',
        'address': '123 Test St',
        'category': 'Test category',
        'status': 'Available',
    }
    # Act / Assert
    with pytest.raises(ValidationError):
        ProductCreationSchema().load(invalid_data)


def test_product_creation_schema_missing_required_fields():
    # Arrange
    invalid_data = {
        'description': 'This is a test product',
        'price': 100,
        'address': '123 Test St',
        'category': 'Test category',
        'status': 'Available',
    }
    # Act / Assert
    with pytest.raises(ValidationError):
        ProductCreationSchema().load(invalid_data)


def test_product_creation_schema_additional_fields():
    # Arrange
    invalid_data = {
        'title': 'Test product',
        'description': 'This is a test product',
        'price': 100,
        'address': '123 Test St',
        'category': 'Test category',
        'status': 'Available',
        'extra_field': 'This is an extra field'
    }
    # Act
    result = ProductCreationSchema().load(invalid_data, unknown=EXCLUDE)
    result = result.__dict__
    # Assert
    assert 'extra_field' not in result


def test_product_creation_schema_file_fields():
    # Arrange

    valid_data = {
        'title': 'Test product',
        'description': 'This is a test product',
        'price': 100,
        'address': '123 Test St',
        'category': 'Test category',
        'status': 'Available'
    }
    # Act
    result = ProductCreationSchema().load(valid_data)
    # Convert valid_data to match the attribute names in the Product class
    result_dict = {
        'title': result.p_title,
        'description': result.p_description,
        'price': result.p_price,
        'address': result.p_address,
        'category': result.p_category,
        'status': result.p_status,
    }
    # Assert
    assert result_dict == valid_data
