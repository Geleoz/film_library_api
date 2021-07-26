from project import db
from project.models import User
from flask_login import login_user, logout_user, current_user


def test_login_logout(client):
    with client:
        user = User(username="test", email="test@gmail.com", password="password")
        db.session.add(user)
        db.session.commit()
        login_user(user)
        assert current_user.username == "test"
        logout_user()
        assert not current_user.is_authenticated
        User.query.filter_by(username="test").delete()
        db.session.commit()
