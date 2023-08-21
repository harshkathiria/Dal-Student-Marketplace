from accounts import db
from accounts.models import tokens_table_name


class UserRole(db.Model):
    __tablename__ = tokens_table_name

    t_id = db.Column(db.Integer, primary_key=True)
    t_token = db.Column(db.String(30), unique=True, nullable=False)
    t_validity = db.Column(db.DateTime(timezone=True), default=db.func.now())
