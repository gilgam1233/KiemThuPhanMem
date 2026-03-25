import enum
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.orm import validates
from Hangy import db, app


class DiscountEnum(enum.Enum):
    PERCENT = 0
    AMOUNT = 1


class OrderStatus(enum.Enum):
    PENDING = 0
    CONFIRMED = 1
    COMPLETED = 2
    CANCELED = 3


class User(db.Model, UserMixin):
    id = db.Column(db.String(10), primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': role
    }


class Admin(User):
    __mapper_args__ = {'polymorphic_identity': 'admin'}

    def can_create_voucher(self): return True


class Shop(User):
    __mapper_args__ = {'polymorphic_identity': 'shop'}

    def can_upload_product(self): return True


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    avatar = db.Column(db.String(100))

    user_id = db.Column(db.String(10), db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('profile', uselist=False))


class Voucher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_type = db.Column(db.Enum(DiscountEnum), nullable=False)
    discount_value = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.now)
    end_date = db.Column(db.DateTime, nullable=False)
    usage_limit = db.Column(db.Integer, default=1)
    is_active = db.Column(db.Boolean, default=True)

    @validates('discount_value')
    def validate_discount(self, key, value):
        if self.discount_type == DiscountEnum.PERCENT and value > 50:
            raise ValueError("Mã giảm giá phần trăm không được quá 50%")
        return value


class UserVoucher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'), nullable=False)
    voucher_id = db.Column(db.Integer, db.ForeignKey('voucher.id'), nullable=False)
    used_given = db.Column(db.Integer, default=1)  # Số lần admin cấp
    current_uses = db.Column(db.Integer, default=0)  # Số lần đã dùng


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(100))


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(10), db.ForeignKey('user.id'), nullable=False)
    voucher_id = db.Column(db.Integer, db.ForeignKey('voucher.id'), nullable=True)

    total_amount = db.Column(db.Float, nullable=False)
    final_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()