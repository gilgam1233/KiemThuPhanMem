
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

# --- CẤU HÌNH CƠ BẢN ---
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/hangydb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = '08032005' #(?)

PAGE_SIZE = 30

login = LoginManager(app)


db = SQLAlchemy(app)

from Hangy.routes.main import main_bp

app.register_blueprint(main_bp)