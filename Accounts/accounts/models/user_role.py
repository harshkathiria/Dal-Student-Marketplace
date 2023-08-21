from accounts import db
from accounts.models import user_role_table_name


class UserRole(db.Model):
    __tablename__ = user_role_table_name

    ur_id = db.Column(db.Integer, primary_key=True)
    ur_name = db.Column(db.String(30), unique = True, nullable= False)

