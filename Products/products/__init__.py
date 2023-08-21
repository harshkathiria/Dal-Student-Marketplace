import os.path

from flask import Flask
from flask_cors import CORS

from products.config import Config
from products.extensions import db
from products.routes.product import products_bp


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(Config)
    app.app_context().push()
    db_user = f"{app.config['DB_USER']}"  # load values from config file
    db_password = f"{app.config['DB_PASSWORD']}"
    db_url = f"{app.config['DB_URL']}"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'''mysql+pymysql://{db_user}:{db_password}@{db_url}'''
    # referenced from https://docs.sqlalchemy.org/en/20/core/engines.html
    db.app = app
    db.init_app(app)

    app.register_blueprint(products_bp)

    return app
