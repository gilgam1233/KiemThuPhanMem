import enum
from datetime import datetime
from Hangy import db
from flask_login import UserMixin
from sqlalchemy import (
    Column,
    Enum,
    Integer,
    Boolean,
    DateTime,
    String,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import validates, relationship


class DiscountEnum(enum.Enum):
    PERCENT = 0
    AMOUNT = 1


class OrderStatus(enum.Enum):
    PENDING = 0
    CONFIRMED = 1
    COMPLETED = 2
    CANCELED = 3


class UserRoleEnum(enum.Enum):
    ADMIN = 0
    USER = 1


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now)


class Category(BaseModel):
    __tablename__ = "categories"
    name = Column(String(50), nullable=False, unique=True)
    products = relationship("Product", backref="category", lazy=True)

    def __str__(self):
        return self.name


class User(BaseModel, UserMixin):
    __tablename__ = "users"
    username = Column(String(30), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    first_name = Column(String(30))
    last_name = Column(String(30))
    email = Column(String(50), unique=True)
    phone = Column(String(15))
    address = Column(String(255))
    avatar = Column(String(255), default="cloudinary_link")  # đưa về cloudinary sau

    orders = relationship("Order", backref="user", lazy=True)
    vouchers = relationship("UserVoucher", backref="user", lazy=True)


class Product(BaseModel):
    __tablename__ = "products"
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String(255), default="cloudinary_link")  # đưa về cloudinary sau

    category_id = Column(Integer, ForeignKey(Category.id))
    order_items = relationship("OrderDetail", backref="product", lazy=True)


class Voucher(BaseModel):
    __tablename__ = "vouchers"

    code = Column(String(50), unique=True, nullable=False)
    discount_type = Column(Enum(DiscountEnum), nullable=False)
    discount_value = Column(Float, nullable=False)
    end_date = Column(DateTime, nullable=False)

    user_vouchers = relationship("UserVoucher", backref="voucher", lazy=True)

    @validates("discount_value")
    def validate_discount(self, key, value):
        if value < 0:
            raise ValueError("Giá trị giảm giá không hợp lệ!")
        if self.discount_type == DiscountEnum.PERCENT and value > 50:
            raise ValueError("Giảm giá phần trăm không được quá 50%!")
        return value


class UserVoucher(BaseModel):
    __tablename__ = "users_vouchers"
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    voucher_id = Column(Integer, ForeignKey(Voucher.id), nullable=False)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=True)

    is_used = Column(Boolean, default=False)
    used_date = Column(DateTime, default=None)


class Order(BaseModel):
    __tablename__ = "orders"
    total_amount = Column(Float, nullable=False)
    final_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship("OrderDetail", backref="order", lazy=True)

    applied_voucher = relationship(
        "UserVoucher", backref="applied_order", uselist=False, lazy=True
    )


class OrderDetail(db.Model):
    __tablename__ = "order_details"

    order_id = Column(Integer, ForeignKey(Order.id), primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), primary_key=True)

    quantity = Column(Integer, nullable=False, default=1)
    price = Column(Float, nullable=False)


if __name__ == "__main__":
    from Hangy import app

    with app.app_context():
        db.create_all()

