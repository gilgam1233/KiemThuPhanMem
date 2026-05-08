from datetime import datetime, timedelta

from test_base import test_app, test_session
import pytest
from Hangy.models import User, Voucher, Order, UserVoucher, OrderStatus, UserRoleEnum
from Hangy.models import DiscountEnum
from datetime import datetime, timedelta
from Hangy.routes.admin import OrderView


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