from marshmallow_sqlalchemy import auto_field, SQLAlchemyAutoSchema, SQLAlchemySchema
from sqlalchemy import BigInteger
from sqlalchemy.orm import relationship

from accounts.models import user_table_name
from accounts import db
from accounts.models.user_role import UserRole


class User(db.Model):
    __tablename__ = user_table_name

    u_id = db.Column(BigInteger, primary_key=True)
    u_name = db.Column(db.String(50), nullable=False)
    u_email = db.Column(db.String(50), unique=True, nullable=False)
    u_password = db.Column(db.Text, nullable=False)
    u_phone = db.Column(db.String(12))
    u_address = db.Column(db.String(100))
    u_postalcode = db.Column(db.String(6))
    u_otp = db.Column(db.Integer)
    u_emailVerified = db.Column(db.Boolean)
    u_role = db.Column(db.Integer, db.ForeignKey(UserRole.ur_id), default=1)
    # default is set to 1 which corresponds to Standard user in user roles

    role = relationship(UserRole.__name__)


class UserSchema(SQLAlchemyAutoSchema):
    u_id = auto_field()
    u_name = auto_field()
    u_email = auto_field()
    u_password = auto_field()
    u_phone = auto_field()
    u_address = auto_field()
    u_postalcode = auto_field()
    u_otp = auto_field()
    u_emailVerified = auto_field()
    u_role = auto_field()

    class Meta:
        model = User
        include_relationships = True
        load_instance = True
