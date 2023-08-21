import os.path

from flask import Flask
from flask_cors import CORS

from accounts.config import Config
from accounts.extensions import db
from accounts.routes.auth import auth_bp
from accounts.routes.error import error_bp
from accounts.routes.health import health_bp
from accounts.routes.users import users_bp


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    app.app_context().push()
    db_user = f"{app.config['DB_USER']}"  # load values from config file
    db_password = f"{app.config['DB_PASSWORD']}"
    db_url = f"{app.config['DB_URL']}"
    app.config["SQLALCHEMY_DATABASE_URI"] = f'''mysql+pymysql://{db_user}:{db_password}@{db_url}'''
    # referenced from https://docs.sqlalchemy.org/en/20/core/engines.html
    db.app = app
    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(error_bp)
    app.register_blueprint(auth_bp)

    return app
