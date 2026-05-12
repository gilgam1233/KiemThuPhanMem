from unittest.mock import MagicMock
from Hangy.services.order_services import order_service
from Hangy.models import User, Voucher, UserVoucher, UserRoleEnum, DiscountEnum, Product, Category
from Hangy.routes.main import voucher_services, order_services
from Hangy.routes.admin import OrderView
from datetime import datetime, timedelta

from test_base import test_app, test_session
import pytest
from Hangy.models import DiscountEnum

def test_unit_apply_voucher_math(test_app,mocker):
    mock_voucher = MagicMock()
    mock_voucher.discount_type = DiscountEnum.PERCENT
    mock_voucher.discount_value = 20

    mocker.patch('Hangy.models.Voucher.query.filter_by',
                 return_value=MagicMock(first=lambda: mock_voucher))
    mocker.patch('Hangy.models.UserVoucher.query.filter_by',
                 return_value=MagicMock(first=lambda: MagicMock(is_used=False)))

    cart = {1: {'id': 1, 'price': 100000, 'quantity': 1}}

    mocker.patch('Hangy.db.session.commit')

    result = order_service.create_order(1, cart, voucher_code='SALE20')

    assert result is True

@pytest.mark.parametrize("valid_data,flag", [
    ({'code': "V001",'discount_type': DiscountEnum.PERCENT, 'discount_value': 10
         , 'end_date': datetime.now() + timedelta(days=1), 'final_amount':90000,
      'amount':100000,'is_active':True,'result':True}, False),
    ({'code': "V001", 'discount_type': DiscountEnum.AMOUNT, 'discount_value': 39999
        , 'end_date': datetime.now() + timedelta(days=1), 'final_amount': 60001,
      'amount': 100000, 'is_active': True,'result':True}, False),
    ({'code': "V001", 'discount_type': DiscountEnum.AMOUNT, 'discount_value': 150000
        , 'end_date': datetime.now() + timedelta(days=1), 'final_amount': 0,
      'amount': 100000, 'is_active': True,'result':True}, False),
    ({'code': "V001", 'discount_type': DiscountEnum.AMOUNT, 'discount_value': 150000
        , 'end_date': datetime.now() + timedelta(days=1), 'final_amount': 0,
      'amount': 100000, 'is_active': True, 'result': True},True)
])
def test_apply_voucher(test_app, test_session,valid_data,flag):
    user = User(username='tester', password='123', role=UserRoleEnum.USER)

    voucher = Voucher(code=valid_data['code'], discount_type=valid_data['discount_type'],
                      discount_value=valid_data['discount_value'], is_active=valid_data['is_active'],
                      end_date=valid_data['end_date'])

    test_session.add_all([user,voucher])
    test_session.flush()

    user_voucher = UserVoucher(user_id=user.id, voucher_id=voucher.id,
                               is_active=True,created_date=datetime.now())

    test_session.add(user_voucher)
    test_session.commit()

    cart = {1: {'id': 1, 'price': valid_data['amount'], 'quantity': 1}}
    result = order_services.create_order(user.id, cart, voucher_code=valid_data['code'])
    assert result is valid_data['result']

    o = order_services.get_order_by_user_id(user.id)

    assert o is not None

    assert o.final_amount == valid_data['final_amount']

    if flag:
        view = OrderView.__new__(OrderView)

        with test_app.test_request_context():
            view.on_model_delete(o)

        test_session.delete(o)
        test_session.commit()

        o = order_services.get_order_by_user_id(user.id)

        assert order_services.load_orders(user.id) == []
        assert ( valid_data['code'] in v for v in voucher_services.load_vouchers(user.id))

        assert o is None


@pytest.mark.parametrize("scenario, voucher_data, uv_data", [
    ("expired",
     {'code': 'OLD_MADD', 'discount_value': 10, 'is_expired': True},
     {'is_used': 0}),

    ("already_used",
     {'code': 'USED_ONCE', 'discount_value': 5000, 'is_expired': False},
     {'is_used': 1})
])
def test_apply_invalid_voucher_scenarios(test_app, test_session, scenario, voucher_data, uv_data):
    user = User(username=f'{scenario}_tester', password='123', role=UserRoleEnum.USER)

    days_offset = -1 if voucher_data['is_expired'] else 1
    voucher = Voucher(
        code=voucher_data['code'],
        discount_type=DiscountEnum.PERCENT if scenario == "expired" else DiscountEnum.AMOUNT,
        discount_value=voucher_data['discount_value'],
        is_active=True,
        end_date=datetime.now() + timedelta(days=days_offset)
    )

    test_session.add_all([user, voucher])
    test_session.flush()

    uv = UserVoucher(
        user_id=user.id,
        voucher_id=voucher.id,
        is_active=True,
        is_used=uv_data['is_used']
    )
    test_session.add(uv)
    test_session.commit()

    assert voucher_services.load_vouchers(user_id=user.id) == []

    cart = {1: {'id': 1, 'price': 100000, 'quantity': 1}}
    result = order_services.create_order(user.id, cart, voucher_code=voucher_data['code'])

    assert result is False

    order = order_services.get_order_by_user_id(user.id)
    assert order is None


@pytest.mark.parametrize("action, expected_result, expected_final_amount", [
    ("change_value", True, 87500),
    ("deactivate", False, None),
    ("remove", False, None)
])
def test_apply_modified_voucher_scenarios(test_app, test_session, action, expected_result, expected_final_amount):
    user = User(username='tester', password='123', role=UserRoleEnum.USER)
    voucher = Voucher(code="V002", discount_type=DiscountEnum.AMOUNT,
                      discount_value=10000, is_active=True,
                      end_date=datetime.now() + timedelta(days=1))
    test_session.add_all([user, voucher])
    test_session.flush()

    uv = UserVoucher(user_id=user.id, voucher_id=voucher.id, is_active=True, created_date=datetime.now())
    test_session.add(uv)
    test_session.commit()

    cart = {1: {'id': 1, 'price': 100000, 'quantity': 1}}

    if action == "change_value":
        voucher.discount_value = 12500
        test_session.commit()
    elif action == "deactivate":
        voucher.is_active = False
        test_session.commit()
    elif action == "remove":
        test_session.delete(uv)
        test_session.commit()

    result = order_services.create_order(user.id, cart, voucher_code="V002")
    assert result is expected_result

    order = order_services.get_order_by_user_id(user.id)

    if expected_result:
        assert order is not None
        assert order.final_amount == expected_final_amount
    else:
        assert order is None
