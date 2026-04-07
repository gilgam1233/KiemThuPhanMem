from flask import request, redirect, url_for, flash
from flask_admin import Admin, expose, AdminIndexView
from flask_admin._compat import text_type
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user, logout_user
from flask_admin.menu import MenuLink
from sqlalchemy import exc

from Hangy import app, db
from Hangy.models import User, Profile, Product, Order, Voucher, UserVoucher


class MyAdminIndexView(AdminIndexView):
    csrf_protection = False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main_bp.login_process', next=request.url))

    @expose('/')
    def index(self):
        return self.render('admin.html')


class MyModelView(ModelView):
    def delete_model(self, model) -> bool:
        try:
            self.on_model_delete(model)
            self.session.flush()
            self.session.delete(model)
            self.session.commit()
        except Exception as ex:
            flash(
                gettext("Xóa dữ liệu thất bại! Vui lòng xem lại ràng buộc bảng dữ liệu", message=text_type(exc)),
                    "error",
            )

            self.session.rollback()

            return False
        else:
            self.after_model_delete(model)

        return True

class UserView(MyModelView):
    column_labels = {
        'id':'ID',
        'username':'USERNAME',
        'password':'PASSWORD',
        'role':'VAI TRÒ'
    }

class ProfileView(MyModelView):
    column_labels = {
        'first_name' : 'TÊN KHÁCH HÀNG',
        'last_name' : 'HỌ KHÁCH HÀNG',
        'email' : 'EMAIL',
        'phone' : 'SỐ ĐIỆN THOẠI',
        'address' : 'ĐỊA CHỈ',
        'avatar' : 'AVATAR'
    }

class ProductView(MyModelView):
    column_labels = {
        'name' : 'TÊN SẢN PHẨM',
        'price' : 'ĐƠN GIÁ',
        'image' : 'ẢNH MINH HỌA SẢN PHẨM'
    }

class OrderView(MyModelView):
    column_list = ['user_id','voucher_id','total_amount','final_amount','status','created_at']
    form_columns = ['user_id','voucher_id','total_amount','final_amount','status','created_at']
    column_labels = {
        'user_id' : 'ID KHÁCH HÀNG',
        'voucher_id' : 'ID VOUCHER',
        'total_amount': 'TỔNG TIỀN',
        'final_amount' : 'THANH TOÁN',
        'status' : 'TRẠNG THÁI',
        'created_at' : 'NGÀY KHỞI TẠO'
    }

class VoucherView(MyModelView):
    column_labels = {
        'code':'MÃ GIẢM GIÁ',
        'discount_type':'LOẠI GIẢM GIÁ',
        'discount_amount':'MỨC GIẢM GIÁ',
        'start_date':'NGÀY BẮT ĐẦU',
        'end_date':'NGÀY KẾT THÚC',
        'usage_limit':'GIỚI HẠN SỬ DỤNG',
        'is_active':'TRẠNG THÁI'
    }

class UserVoucherView(MyModelView):
    column_list = ['user_id','voucher_id','used_given','current_uses']
    form_columns = ['user_id','voucher_id','used_given','current_uses']
    column_labels = {
        'user_id' : 'ID KHÁCH HÀNG',
        'voucher_id' : 'ID VOUCHER',
        'used_given' : 'SỐ LƯỢT ĐƯỢC CẤP',
        'current_uses' : 'SỐ LẦN SỬ DỤNG'
    }

admin = Admin(
    app=app,
    theme=Bootstrap4Theme(),
    index_view=MyAdminIndexView(),
    name='E-COMMERCE',
)


admin.add_view(UserView(User, db.session, name='Người dùng'))
admin.add_view(ProfileView(Profile, db.session, name='Hồ sơ'))
admin.add_view(ProductView(Product, db.session, name='Sản phẩm'))
admin.add_view(OrderView(Order, db.session, name='Đơn hàng'))
admin.add_view(VoucherView(Voucher, db.session, name='Mã giảm giá'))
admin.add_view(UserVoucherView(UserVoucher, db.session, name='UserVoucher'))

admin.add_link(MenuLink(name='Đăng xuất', url='/logout'))