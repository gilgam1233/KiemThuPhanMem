from unittest.mock import MagicMock
from test_base import test_app
import pytest
from Hangy.models import Order, UserVoucher, OrderStatus
from Hangy.routes.admin import OrderView


def test_unit_admin_delete_order_resets_voucher(test_app, mocker):
    mock_order = MagicMock(spec=Order)
    mock_order.id = 999

    mock_user_voucher = MagicMock(spec=UserVoucher)
    mock_user_voucher.is_used = 1


    mock_uv_query = mocker.patch('Hangy.routes.admin.UserVoucher.query')
    mock_uv_query.filter_by.return_value.first.return_value = mock_user_voucher

    stub_order = MagicMock()
    stub_order.status = OrderStatus.PENDING
    mocker.patch('Hangy.routes.admin.order_services.get_order_by_id', return_value=stub_order)

    mocker.patch('Hangy.routes.admin.OrderDetail.query')

    mocker.patch('Hangy.db.session')

    view = OrderView.__new__(OrderView)
    view.on_model_delete(mock_order)

    assert mock_user_voucher.is_used == 0
    assert mock_user_voucher.order_id is None