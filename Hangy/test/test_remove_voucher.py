from test_base import test_app, test_session

from unittest.mock import MagicMock
import pytest
from Hangy.models import User, Voucher, Order, UserVoucher, OrderStatus, UserRoleEnum
from Hangy.models import DiscountEnum
from datetime import datetime, timedelta
from Hangy.routes.admin import OrderView

@pytest.mark.parametrize("order_status, has_voucher, expected_is_used, should_raise", [
    (OrderStatus.PENDING, True, 0, False),

    (OrderStatus.COMPLETED, True, 1, True),

    (OrderStatus.PENDING, False, None, False),
])
def test_unit_admin_delete_order_logic(test_app, mocker, order_status, has_voucher, expected_is_used, should_raise):
    mock_order = MagicMock(spec=Order)
    mock_order.id = 999

    mock_user_voucher = None
    if has_voucher:
        mock_user_voucher = MagicMock(spec=UserVoucher)
        mock_user_voucher.is_used = 1
        mock_user_voucher.order_id = 999

    mocker.patch('Hangy.routes.admin.UserVoucher.query').filter_by.return_value.first.return_value = mock_user_voucher

    stub_order = MagicMock()
    stub_order.status = order_status
    mocker.patch('Hangy.routes.admin.order_services.get_order_by_id', return_value=stub_order)
    mocker.patch('Hangy.routes.admin.OrderDetail.query')
    mocker.patch('Hangy.db.session')

    view = OrderView.__new__(OrderView)

    if should_raise:
        with pytest.raises(Exception, match="Không thể xóa đơn hàng"):
            view.on_model_delete(mock_order)
        if has_voucher:
            assert mock_user_voucher.is_used == 1
    else:
        view.on_model_delete(mock_order)
        if has_voucher:
            assert mock_user_voucher.is_used == expected_is_used
            assert mock_user_voucher.order_id is None

def test_admin_delete_completed_order_fails(test_app, test_session):
    order = Order(id=99, user_id=1, status=OrderStatus.COMPLETED,
                  total_amount=100, final_amount=100)
    test_session.add(order)
    test_session.commit()

    view = OrderView(Order, test_session)

    with pytest.raises(Exception) as excinfo:
        view.on_model_delete(order)

    assert "Không thể xóa đơn hàng!!!" in str(excinfo.value)

def test_admin_delete_order_resets_voucher(test_app, test_session):

    user = User(id=1, username='test_admin', password='123', role=UserRoleEnum.ADMIN)
    test_session.add(user)

    voucher = Voucher(
        id=1,
        code='TEST_CODE',
        discount_type=DiscountEnum.AMOUNT,
        discount_value=30000,
        is_active=True,
        end_date=datetime.now() + timedelta(days=1)
    )
    test_session.add(voucher)

    test_session.flush()

    order = Order(
        id=1,
        user_id=user.id,
        status=OrderStatus.PENDING,
        total_amount=100000,
        final_amount=70000
    )

    uv = UserVoucher(
        user_id=user.id,
        voucher_id=voucher.id,
        order_id=order.id,
        is_used=1
    )

    test_session.add_all([order, uv])
    test_session.commit()

    view = OrderView(Order, test_session)
    view.on_model_delete(order)

    assert uv.is_used == 0
    assert uv.order_id is None