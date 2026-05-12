from test_base import test_app, test_session
from Hangy.routes.main import voucher_services
from sqlalchemy.exc import IntegrityError
import pytest
from Hangy.models import DiscountEnum, Voucher
from datetime import datetime


@pytest.mark.parametrize("d_type, d_value, end_date", [
    (DiscountEnum.PERCENT, 55,None),
    (DiscountEnum.PERCENT, -10,None),
    (DiscountEnum.AMOUNT, -5000,None),
    (DiscountEnum.AMOUNT, 0,None),
    (DiscountEnum.PERCENT, 10, datetime.strptime('2026-05-01 23:26:26', '%Y-%m-%d %H:%M:%S')),
    (DiscountEnum.PERCENT, 30,'aa/b@/c!de 12:00 de'),
    ('ABC!@123', 30,None),

])
def test_create_invalid_voucher(d_type, d_value,end_date):
    actual_end_date = end_date or datetime.now()
    with pytest.raises(ValueError):
        voucher_services.validate_voucher_rules(d_type, d_value,actual_end_date)

def test_create_valid_voucher():
    assert voucher_services.validate_voucher_rules(DiscountEnum.PERCENT, 30) is True

@pytest.mark.parametrize("invalid_data, setup_duplicate", [
    ({}, False),
    ({'discount_type': DiscountEnum.PERCENT, 'discount_value': 10, 'end_date': datetime.now()}, False),
    ({'code': "TEST01", 'discount_value': 10, 'end_date': datetime.now()}, False),
    ({'code': "TEST02", 'discount_type': DiscountEnum.AMOUNT, 'end_date': datetime.now()},False),
    ({'code': "TEST03", 'discount_type': DiscountEnum.AMOUNT, 'discount_value': 20},False),
    ({'code': "TEST04", 'discount_type': DiscountEnum.PERCENT, 'discount_value': 6, 'end_date': datetime.now()},True)
])
def test_voucher_integrity_constraints(test_session, invalid_data, setup_duplicate):
    if setup_duplicate:
        existing_v = Voucher(
            code=invalid_data['code'],
            discount_type=DiscountEnum.AMOUNT,
            discount_value=10,
            end_date=datetime.now()
        )
        test_session.add(existing_v)
        test_session.commit()

    v = Voucher(**invalid_data)
    test_session.add(v)

    with pytest.raises(IntegrityError):
        test_session.commit()

    test_session.rollback()
