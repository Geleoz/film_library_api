from project import db, login_manager
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Status(db.Model):
    __tablename__ = "status"

    status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    users = relationship("User", back_populates="status")

    def __init__(self, name):
        self.name = name


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'))
    status = relationship("Status", back_populates="users")

    def get_id(self):
        return self.user_id

