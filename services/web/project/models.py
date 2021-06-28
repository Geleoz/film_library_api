from project import db
from sqlalchemy.orm import relationship


class Status(db.Model):
    __tablename__ = "status"

    status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)
    users = relationship("User", back_populates="status")

    def __init__(self, name):
        self.name = name


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.status_id'))
    status = relationship("Status", back_populates="users")

