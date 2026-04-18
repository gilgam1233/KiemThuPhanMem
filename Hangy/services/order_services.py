from datetime import datetime
from typing import List, Dict, Tuple

from flask import jsonify

from Hangy import db
from Hangy.models import Order, OrderStatus, OrderDetail, DiscountEnum, UserVoucher, Voucher
from Hangy.routes.main import voucher_services

class OrderService:

    def get_order_by_id(self, id: int) -> Order:
        return Order.query.filter_by(id=id).first()


    def payment(self,order:Order):
        try:
            order.status = OrderStatus.COMPLETED

            user_voucher = UserVoucher.query.filter_by(order_id=order.id).first()
            if user_voucher:
                user_voucher.is_used = True
                user_voucher.used_date = datetime.now()

            db.session.commit()

            return jsonify({
                "status": "success",
                "message": "Thanh toán giả lập thành công!",
                "order_id": order.id,
                "final_amount": order.final_amount
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"Lỗi hệ thống: {str(e)}"}), 500

    def create_order(self, user_id, cart_items, voucher_code=None) -> bool:
        try:
            voucher = voucher_services.get_voucher_by_code_name(voucher_code)
            total_amount = sum(item['quantity'] * item['price'] for item in cart_items.values())

            final_amount = total_amount
            user_voucher_to_update = None
            if voucher:
                v_info = (UserVoucher.query
                          .join(Voucher, UserVoucher.voucher_id == Voucher.id)
                          .filter(
                    Voucher.code == voucher.code,
                    UserVoucher.user_id == user_id,
                    UserVoucher.is_used == 0,
                    Voucher.is_active == 1
                ).first())
                if v_info:
                    user_voucher_to_update = v_info

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
                user_voucher_to_update.is_used = 1
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
