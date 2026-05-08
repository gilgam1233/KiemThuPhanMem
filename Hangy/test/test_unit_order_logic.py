from unittest.mock import MagicMock
from Hangy.services.order_services import order_service
from Hangy.models import DiscountEnum
from Hangy.test.test_base import test_app

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