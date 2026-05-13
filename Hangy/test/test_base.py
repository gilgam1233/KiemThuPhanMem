import pytest
from flask import Flask
from flask_admin import Admin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from Hangy import db
from Hangy.models import Voucher
from Hangy.routes.admin import VoucherView


def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["PAGE_SIZE"]=30
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SECRET_KEY'] = 'testsecret'

    db.init_app(app)

    admin = Admin(app, name='Hangy Admin')
    admin.add_view(VoucherView(Voucher, db.session))

    return app

@pytest.fixture
def test_app():
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def test_session(test_app):
    yield db.session
    db.session.rollback()

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.set_window_size(1366, 768)
    yield driver
    driver.quit()