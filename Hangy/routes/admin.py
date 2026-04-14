import typing as t

from flask import request, redirect, url_for, flash
from flask_admin import Admin, expose, AdminIndexView
from flask_admin._compat import text_type
from flask_admin._types import T_SQLALCHEMY_MODEL
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user
from flask_admin.menu import MenuLink
from wtforms import Form

from Hangy import app, db
from Hangy.models import User, Product, Order, Voucher, UserVoucher, Category, UserRoleEnum, OrderDetail
from Hangy.services.validators import validate_voucher_rules


class MyAdminIndexView(AdminIndexView):
    csrf_protection = False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == UserRoleEnum.ADMIN

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main_bp.login_process', next=request.url))

    @expose('/')
    def index(self):
        return self.render('admin.html')


class MyModelView(ModelView):
    column_display_pk = True

    def delete_model(self, model) -> bool:
        try:
            self.on_model_delete(model)
            self.session.flush()
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            flash(
                gettext("Xóa dữ liệu thất bại! Vui lòng xem lại ràng buộc bảng dữ liệu",
                        message=text_type(ex)), "error",
            )
            self.session.rollback()
            return False
        else:
            self.after_model_delete(model)
        return True

    def create_model(self, form: Form):
        try:
            model = self.build_new_instance()

            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except ValueError as ex:
            flash(str(ex), "error")
            self.session.rollback()
            return False
        except Exception as ex:
            flash(
                gettext("Tạo dữ liệu thất bại! Vui lòng xem lại ràng buộc bảng dữ liệu", message=text_type(ex)), "error"
            )
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, True)
        return model

    def update_model(self, form: Form, model: T_SQLALCHEMY_MODEL) -> bool:
        try:
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            self.session.commit()
        except ValueError as ex:
            flash(str(ex), "error")
            self.session.rollback()
            return False
        except Exception as ex:
            flash(
                gettext("Failed to update record. %(error)s", error=str(ex)),
                "error",
            )
            self.session.rollback()
            return False
        else:
            self.after_model_change(form, model, False)
        return True



class UserView(MyModelView):
    column_list = ['id', 'username', 'role', 'first_name', 'last_name', 'email', 'phone']
    column_labels = {
        'id': 'ID',
        'username': 'Tên đăng nhập',
        'role': 'Vai trò',
        'first_name': 'Tên',
        'last_name': 'Họ',
        'email': 'Email',
        'phone': 'Số điện thoại',
        'address': 'Địa chỉ'
    }


class CategoryView(MyModelView):
    column_labels = {'name': 'Tên danh mục'}


class ProductView(MyModelView):
    column_list = ['id', 'name', 'price', 'category']
    column_labels = {
        'id': 'ID',
        'name': 'Tên sản phẩm',
        'price': 'Đơn giá',
        'image': 'Ảnh',
        'category': 'Danh mục'
    }


class OrderView(MyModelView):
    column_list = ['id', 'user', 'total_amount', 'final_amount', 'status', 'created_date']
    column_labels = {
        'id': 'Mã đơn hàng',
        'user': 'Khách hàng',
        'total_amount': 'Tổng tiền',
        'final_amount': 'Thanh toán',
        'status': 'Trạng thái',
        'created_date': 'Ngày tạo'
    }

class OrderDetailView(MyModelView):
    column_list = ['created_date','quantity','price','product','order']
    column_labels = {
        'created_date': 'Ngày tạo',
        'quantity': 'Số lượng',
        'price': 'Đơn giá',
        'product': 'Sản phẩm',
        'order': 'Đơn hàng'
    }


class VoucherView(MyModelView):
    column_labels = {
        'code': 'Mã giảm giá',
        'discount_type': 'Loại (Phần trăm/Số tiền)',
        'discount_value': 'Mức giảm',
        'end_date': 'Ngày hết hạn'
    }

    def on_model_change(self, form, model, is_created):
        validate_voucher_rules(model.discount_type, model.discount_value, model.end_date)

        super().on_model_change(form, model, is_created)


class UserVoucherView(MyModelView):
    column_list = ['user', 'voucher', 'is_used', 'used_date']
    column_labels = {
        'user': 'Khách hàng',
        'voucher': 'Mã áp dụng',
        'is_used': 'Đã sử dụng',
        'used_date': 'Ngày dùng'
    }


admin = Admin(
    app=app,
    theme=Bootstrap4Theme(),
    index_view=MyAdminIndexView(),
    name='HANGY ADMIN',
)

# Đăng ký các View với Model tương ứng
admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(CategoryView(Category, db.session, name='Danh mục'))
admin.add_view(ProductView(Product, db.session, name='Sản phẩm'))
admin.add_view(OrderView(Order, db.session, name='Đơn hàng'))
admin.add_view(OrderDetailView(OrderDetail, db.session, name='Chi tiết đơn hàng'))
admin.add_view(VoucherView(Voucher, db.session, name='Kho mã giảm giá'))
admin.add_view(UserVoucherView(UserVoucher, db.session, name='Voucher người dùng'))

admin.add_link(MenuLink(name='Về Trang Chủ', url='/'))
admin.add_link(MenuLink(name='Đăng xuất', url='/logout'))