import pytest
from flask import Flask, url_for

from products import create_app, db
from products.routes.product import products_bp


def test_create_app():
    # Act
    app = create_app()
    # Assert
    assert isinstance(app, Flask)
    assert app.config['DEBUG'] is False


def test_create_app_with_test_config():
    # Arrange
    class TestConfig:
        DEBUG = True
        TESTING = True

    # Act
    app = create_app()
    # Assert
    assert isinstance(app, Flask)
    assert app.config['DEBUG'] is False


def test_create_app_with_wrong_config_object():
    # Arrange
    wrong_config = "Not a config object"
    # Act / Assert
    with pytest.raises(TypeError):
        create_app(config_object=wrong_config)


@pytest.fixture(scope="session")
def flask_app():
    app = create_app()

    client = app.test_client()

    ctx = app.test_request_context()
    ctx.push()

    yield client

    ctx.pop()


@pytest.fixture(scope="session")
def app_with_db(flask_app):
    db.create_all()

    yield flask_app

    db.session.commit()
    db.drop_all()


@pytest.fixture(scope='session')
def test_client():
    class TestConfig:
        DEBUG = True
        TESTING = True
        SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    app = create_app(TestConfig)
    app.register_blueprint(products_bp)

    with app.test_client() as testing_client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
        yield testing_client

    with app.app_context():
        db.session.remove()
        db.drop_all()
