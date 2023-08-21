import pytest
from marshmallow import ValidationError, EXCLUDE

from products.dto.product_change import ProductUpdateSchema


def test_valid_product_update_schema():
    # Arrange
    valid_data = {
        'product_id': 123,
        'status': 'New',
    }
    # Act
    result = ProductUpdateSchema().load(valid_data)
    # Assert
    assert result.product_id == valid_data['product_id']
    assert result.status == valid_data['status']


def test_invalid_product_update_schema():
    # Arrange
    invalid_data = {
        'product_id': 'invalid_id',
        'status': 'sold',
    }
    # Act / Assert
    with pytest.raises(ValidationError):
        ProductUpdateSchema().load(invalid_data)


def test_product_update_schema_missing_required_fields():
    # Arrange
    invalid_data = {
        'status': 'sold',
    }
    # Act / Assert
    with pytest.raises(ValidationError):
        ProductUpdateSchema().load(invalid_data)


def test_product_update_schema_additional_fields():
    # Arrange
    invalid_data = {
        'product_id': 123,
        'status': 'Available',
        'extra_field': 'This is an extra field'
    }
    # Act
    result = ProductUpdateSchema().load(invalid_data, unknown=EXCLUDE)
    result = result.__dict__
    # Assert
    assert 'extra_field' not in result


def test_product_update_object():
    # Arrange
    valid_data = {
        'product_id': 123,
        'status': 'Available',
    }
    # Act
    product_update = ProductUpdateSchema().load(valid_data)
    # Assert
    assert product_update.product_id == valid_data['product_id']
    assert product_update.status == valid_data['status']
