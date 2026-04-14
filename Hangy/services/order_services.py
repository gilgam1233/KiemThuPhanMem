from datetime import datetime
from typing import List

from Hangy import db
from Hangy.models import Order, OrderStatus, OrderDetail, DiscountEnum, UserVoucher, Voucher


class OrderService:
    def create_order(self, user_id, cart_items, voucher_code=None):
        try:
            total_amount = sum(item['quantity'] * item['price'] for item in cart_items.values())
            final_amount = total_amount
            user_voucher_to_update = None

            if voucher_code:
                v_info = (db.session.query(Voucher, UserVoucher)
                          .join(UserVoucher, Voucher.id == UserVoucher.voucher_id)
                          .filter(
                    Voucher.code == voucher_code,
                    UserVoucher.user_id == user_id,
                    UserVoucher.is_used == False,
                    Voucher.is_active == True
                ).first())

                if v_info:
                    voucher, user_voucher = v_info
                    user_voucher_to_update = user_voucher

                    if voucher.discount_type == DiscountEnum.PERCENT:
                        discount = total_amount * (voucher.discount_value / 100)
                    else:
                        discount = voucher.discount_value

                    final_amount = max(0, total_amount - discount)

            new_order = Order(
                user_id=user_id,
                total_amount=total_amount,
                final_amount=final_amount,
                status=OrderStatus.PENDING
            )
            db.session.add(new_order)
            db.session.flush()

            for item in cart_items.values():
                detail = OrderDetail(
                    order_id=new_order.id,
                    product_id=item['id'],
                    quantity=item['quantity'],
                    price=item['price']
                )
                db.session.add(detail)

            if user_voucher_to_update:
                user_voucher_to_update.is_used = True
                user_voucher_to_update.used_date = datetime.now()
                user_voucher_to_update.order_id = new_order.id

            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            print(f"Lỗi tạo đơn hàng: {e}")
            return False

    def load_orders(self, id: int) -> List[Order]:
        return Order.query.filter_by(user_id=id).order_by(Order.created_date.desc()).all()

order_service = OrderService()
