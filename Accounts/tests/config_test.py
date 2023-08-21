import os

from accounts.config import Config, DevelopmentConfig, ProductionConfig


def test_config():
    # Set up test data
    os.environ["DB_URL"] = "test_db_url"
    os.environ["DB_USER"] = "test_db_user"
    os.environ["DB_PASSWORD"] = "test_db_password"
    os.environ["MAIL_USERNAME"] = "test_mail_username"
    os.environ["MAIL_PASSWORD"] = "test_mail_password"
    os.environ["HASH_SECRET"] = "test_hash_secret"

    # Create config object
    config = Config()

    # Verify object attributes
    assert config.DEBUG == False
    assert config.TESTING == False
    assert config.SQLALCHEMY_DATABASE_URI == "test_db_url"
    assert config.DB_USER == "test_db_user"
    assert config.DB_PASSWORD == "test_db_password"
    assert config.DB_URL == "test_db_url"
    assert config.MAIL_SERVER == "smtp.gmail.com"
    assert config.MAIL_PORT == 465
    assert config.MAIL_USERNAME == "test_mail_username"
    assert config.MAIL_PASSWORD == "test_mail_password"
    assert config.HASH_SECRET == "test_hash_secret"


def test_development_config():
    # Set up test data
    os.environ["DB_URL"] = "test_db_url"
    os.environ["DB_USER"] = "test_db_user"
    os.environ["DB_PASSWORD"] = "test_db_password"
    os.environ["MAIL_USERNAME"] = "test_mail_username"
    os.environ["MAIL_PASSWORD"] = "test_mail_password"
    os.environ["HASH_SECRET"] = "test_hash_secret"

    # Create development config object
    config = DevelopmentConfig()

    # Verify object attributes
    assert config.ENV == "development"
    assert config.DEVELOPMENT == True
    assert config.DEBUG == False
    assert config.TESTING == False
    assert config.SQLALCHEMY_DATABASE_URI == "test_db_url"
    assert config.DB_USER == "test_db_user"
    assert config.DB_PASSWORD == "test_db_password"
    assert config.DB_URL == "test_db_url"
    assert config.MAIL_SERVER == "smtp.gmail.com"
    assert config.MAIL_PORT == 465
    assert config.MAIL_USERNAME == "test_mail_username"
    assert config.MAIL_PASSWORD == "test_mail_password"
    assert config.HASH_SECRET == "test_hash_secret"


def test_production_config():
    # Set up test data
    os.environ["DB_URL"] = "test_db_url"
    os.environ["DB_USER"] = "test_db_user"
    os.environ["DB_PASSWORD"] = "test_db_password"
    os.environ["MAIL_USERNAME"] = "test_mail_username"
    os.environ["MAIL_PASSWORD"] = "test_mail_password"
    os.environ["HASH_SECRET"] = "test_hash_secret"

    # Create production config object
    config = ProductionConfig()

    # Verify object attributes
    assert config.DATABASE_URI == ""
