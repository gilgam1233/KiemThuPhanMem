from test_base import test_app, test_session
import pytest
from Hangy.services.admin_services import validate_voucher_rules
from Hangy.models import DiscountEnum

@pytest.mark.parametrize("d_type, d_value", [
    (DiscountEnum.PERCENT, 55),
    (DiscountEnum.PERCENT, -10),
    (DiscountEnum.AMOUNT, -5000)
])
def test_admin_create_invalid_voucher(d_type, d_value):
    with pytest.raises(ValueError):
        validate_voucher_rules(d_type, d_value)

def test_admin_create_valid_voucher():
    assert validate_voucher_rules(DiscountEnum.PERCENT, 30) is True
