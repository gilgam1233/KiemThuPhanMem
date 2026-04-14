from datetime import datetime
from Hangy.models import DiscountEnum

def validate_voucher_rules(discount_type, discount_value, end_date=None):

    if discount_value < 0:
        raise ValueError("Lỗi: Giá trị giảm giá không được là số âm!")

    is_percent = discount_type == DiscountEnum.PERCENT or str(discount_type) == 'PERCENT' or str(discount_type) == 'DiscountEnum.PERCENT'

    if is_percent and discount_value > 50:
        raise ValueError("Lỗi: Mức giảm giá phần trăm không được vượt quá 50%!")

    if end_date:
        if end_date.date() < datetime.now().date():
            raise ValueError("Lỗi: Thời gian hiệu lực phải lớn hơn hoặc bằng ngày hiện tại!")

    return True