import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())

# --- CẤU HÌNH CƠ BẢN ---

PAGE_SIZE = 30


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv("DATABASE_USER","root")}:{os.getenv("DATABASE_PASSWORD","123456")}@{os.getenv("DATABASE_HOST","localhost")}/{os.getenv("DATABASE_NAME","hangydb")}?charset=utf8mb4"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.secret_key = os.getenv("APP_SECRET_KEY", "08032005")


    db = SQLAlchemy()

    try:
        from Hangy.routes.main import main_bp

        app.register_blueprint(main_bp)

    except ImportError as ex:
        raise ImportError(f"Lỗi import: {ex}")
    except Exception as e:
        raise Exception(f"Lỗi chung: {e}")

    return app, db, login


app, db, login = create_app()
