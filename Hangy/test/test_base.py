import pytest
from flask import Flask
from selenium import webdriver

from Hangy import db

def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["PAGE_SIZE"]=30
    db.init_app(app)

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
    driver.maximize_window()
    yield driver
    driver.quit()