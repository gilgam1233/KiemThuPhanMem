from datetime import datetime, timedelta

from test_base import test_app, test_session
import pytest
from Hangy.services.admin_services import validate_voucher_rules
from Hangy.models import DiscountEnum

def test_apply_expired_voucher(test_app, test_session):
    from Hangy.models import User, Voucher, UserVoucher, UserRoleEnum, DiscountEnum
    from Hangy.services.order_services import order_service
    from datetime import datetime, timedelta

    user = User(username='expired_tester', password='123', role=UserRoleEnum.USER)
    voucher = Voucher(code='OLD_MADD', discount_type=DiscountEnum.PERCENT,
                      discount_value=10, is_active=True,
                      end_date=datetime.now() - timedelta(days=1))
    test_session.add_all([user, voucher])
    test_session.commit()

    cart = {1: {'id': 1, 'price': 100, 'quantity': 1}}
    result = order_service.create_order(user.id, cart, voucher_code='OLD_MADD')
    assert result is False

def test_apply_already_used_voucher(test_app, test_session):
    from Hangy.models import User, Voucher, UserVoucher, UserRoleEnum
    from Hangy.services.order_services import order_service

    user = User(username='used_tester', password='123', role=UserRoleEnum.USER)
    voucher = Voucher(code='USED_ONCE', discount_type=DiscountEnum.AMOUNT,
                      discount_value=5000, is_active=True, end_date=datetime.now() + timedelta(days=1))
    test_session.add_all([user, voucher])
    test_session.commit()

    uv = UserVoucher(user_id=user.id, voucher_id=voucher.id, is_used=1)
    test_session.add(uv)
    test_session.commit()

    cart = {1: {'id': 1, 'price': 100, 'quantity': 1}}
    result = order_service.create_order(user.id, cart, voucher_code='USED_ONCE')
    assert result is False

def test_user_apply_voucher_success(test_app, test_session):
    from Hangy.models import User, Voucher, UserVoucher, UserRoleEnum, Product, Category, DiscountEnum
    from Hangy.services.order_services import order_service
    from datetime import datetime, timedelta

    cat = Category(name="Điện thoại")
    test_session.add(cat)
    test_session.flush()

    prod = Product(id=1, name='SP1', price=100000, category_id=cat.id)
    test_session.add(prod)

    user = User(username='khachhang1', password='123', role=UserRoleEnum.USER)
    voucher = Voucher(
        code='SALE30',
        discount_type=DiscountEnum.PERCENT,
        discount_value=30,
        is_active=True,
        end_date=datetime.now() + timedelta(days=30)
    )
    test_session.add_all([user, voucher])
    test_session.commit()

    uv = UserVoucher(user_id=user.id, voucher_id=voucher.id, is_used=False)
    test_session.add(uv)
    test_session.commit()

    cart = {1: {'id': 1, 'name': 'SP1', 'price': 100000, 'quantity': 1}}

    result = order_service.create_order(user.id, cart, voucher_code='SALE30')
    assert result is True

    from Hangy.models import Order
    order = Order.query.filter_by(user_id=user.id).first()
    assert order is not None
    assert order.final_amount == 70000