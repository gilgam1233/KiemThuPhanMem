from typing import List
from Hangy.models import Voucher, UserVoucher, User

class VoucherService:
    def load_vouchers(self, user_id: int) -> List[Voucher] | None:
        try:
            if not user_id or user_id <= 0:
                raise ValueError("ID người dùng không hợp lệ!")

            user = User.query.get(user_id)
            if not user:
                raise ValueError(f"Không tìm thấy người dùng với ID: {user_id}")

            vouchers = UserVoucher.query.filter_by(user_id=user_id, is_used =0).all()
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

voucher_service = VoucherService()