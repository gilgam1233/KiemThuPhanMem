from datetime import datetime, timedelta
from test_base import test_app, test_session
from Hangy.models import Voucher, DiscountEnum
from Hangy.services.admin_services import validate_voucher_rules


def test_integration_admin_save_voucher(test_app, test_session):
    d_type = DiscountEnum.PERCENT
    d_value = 30
    end_date = datetime.now() + timedelta(days=5)

    isValid = validate_voucher_rules(d_type, d_value, end_date)
    assert isValid is True

    if isValid:
        new_v = Voucher(
            code="SAVE_TO_DB",
            discount_type=d_type,
            discount_value=d_value,
            end_date=end_date,
            is_active=True
        )
        test_session.add(new_v)
        test_session.commit()

    v_in_db = Voucher.query.filter_by(code="SAVE_TO_DB").first()
    assert v_in_db is not None
    assert v_in_db.discount_value == 30