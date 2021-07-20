from project import app
from pytest import fixture
from flask.testing import FlaskClient

@fixture(scope='module')
def test_client():
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@fixture(scope='module')
def flask_app():
    with app.app_context():
        yield app


@fixture(scope='module')
def client(flask_app):
    app = flask_app
    ctx = flask_app.test_request_context()
    ctx.push()
    app.test_client_class = FlaskClient
    return app.test_client()
