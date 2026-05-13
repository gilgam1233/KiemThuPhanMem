from datetime import datetime
from typing import List
from Hangy.models import Voucher, UserVoucher, User, DiscountEnum


class VoucherService:
    def load_vouchers(self, user_id: int) -> List[Voucher] | None:
        try:
            if not user_id or user_id <= 0:
                raise ValueError("ID người dùng không hợp lệ!")

            user = User.query.get(user_id)
            if not user:
                raise ValueError(f"Không tìm thấy người dùng với ID: {user_id}")

            vouchers = UserVoucher.query.join(Voucher).filter(UserVoucher.user_id==user_id, UserVoucher.is_used ==0,
                                                              UserVoucher.voucher_id== Voucher.id,
                                                              Voucher.end_date>=datetime.now()).all()
            return vouchers

        except ValueError as ve:
            print(f"Lỗi logic: {ve}")
            return None
        except Exception as e:
            print(f"Lỗi hệ thống khi load voucher: {e}")
            return None

    def get_voucher_by_id(self, voucher_id: int) -> Voucher | None:
        try:
            voucher = Voucher.query.get(voucher_id)
            if not voucher:
                return None
            return voucher
        except Exception as ex:
            print(f'Lỗi chung: {ex}')

    def get_voucher_by_code_name(self, code_name: str) -> Voucher | None:
        try:
            voucher = Voucher.query.filter_by(code=code_name).first()
            if not voucher:
                return None
            return voucher
        except Exception as ex:
            print(f'Lỗi chung: {ex}')

    def validate_voucher_rules(self,discount_type, discount_value, end_date=None):

        if discount_value:
            try:
                val = float(discount_value)
            except ValueError:
                raise ValueError("Lỗi: Định dạng giá trị giảm không đúng (chứa ký tự chữ hoặc ký hiệu lạ)")

        if isinstance(end_date, str):
            try:
                datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                raise ValueError("Lỗi: Định dạng ngày tháng không đúng")

        if isinstance(discount_type, str):
            try:
                discount_type = DiscountEnum[discount_type.upper()]

            except KeyError:
                raise ValueError("Lỗi: Enum không tồn tại giá trị")

        if discount_value <= 0:
            raise ValueError("Lỗi: Giá trị giảm giá không được là số âm!")

        is_percent = discount_type == DiscountEnum.PERCENT or str(discount_type) == 'PERCENT' or str(
            discount_type) == 'DiscountEnum.PERCENT'

        if is_percent and discount_value > 50:
            raise ValueError("Lỗi: Mức giảm giá phần trăm không được vượt quá 50%!")

        if end_date:
            if end_date.date() < datetime.now().date():
                raise ValueError("Lỗi: Thời gian hiệu lực phải lớn hơn hoặc bằng ngày hiện tại!")

        return True


voucher_service = VoucherService()