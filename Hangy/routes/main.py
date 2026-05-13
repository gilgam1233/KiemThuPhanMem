import math
from functools import wraps

from flask import render_template, request, redirect, url_for, flash, Blueprint, session, jsonify, abort
from sqlalchemy.sql.functions import current_user
from flask_login import login_user, logout_user, current_user, login_required

from Hangy import PAGE_SIZE, login
from Hangy.models import UserRoleEnum, OrderStatus
from Hangy.services.user_services import user_service as user_services
from Hangy.services.product_services import product_service as product_services
from Hangy.services.voucher_services import voucher_service as voucher_services
from Hangy.services.order_services import order_service as order_services

main_bp = Blueprint("main_bp", __name__, template_folder="../templates/Main_Page")

@main_bp.context_processor
def inject_cart_data():
    cart = session.get('cart', {})
    total_quantity = sum(item['quantity'] for item in cart.values())

    return dict(total_quantity=total_quantity)

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('main_bp.login_process'))

            if current_user.role != role:
                if current_user.role == UserRoleEnum.ADMIN:
                    return redirect(url_for('admin.index'))
                else:
                    return abort(403)

            return f(*args, **kwargs)

        return decorated_function

    return decorator

@main_bp.route("/")
def index():
    if current_user.is_authenticated and current_user.role == UserRoleEnum.ADMIN:
        return redirect(url_for('admin.index'))

    kw = request.args.get("kw")

    page = request.args.get("page", 1, type=int)

    page_size = PAGE_SIZE

    list_products, total = product_services.load_products(kw=kw, page=page, page_size=page_size)
    total_pages = math.ceil(total / page_size)

    return render_template(
        "index.html",
        list_products=list_products,
        total_pages=total_pages,
        current_user=current_user,
        current_page=page
    )


# ==========================================
# LOGIN / LOGOUT / LOAD USER
# ==========================================
@login.user_loader
def load_user(user_id):
    return user_services.get_user_by_id(int(user_id))


@main_bp.route("/login", methods=["GET", "POST"])
def login_process():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = user_services.authenticate(username=username, password=password)

        if user:
            login_user(user)

            if current_user.role == 'ADMIN':
                return redirect(url_for("admin.index"))

            return {"status": "success", "next": request.args.get("next") or url_for("main_bp.index")}, 200
        else:
            return {"status": "error", "message": "Tài khoản hoặc mật khẩu không đúng!"}, 400

    return render_template("login.html")


@main_bp.route("/logout")
def logout_process():
    logout_user()
    return redirect(url_for("main_bp.login_process"))


# ==========================================
# REGISTER
# ==========================================


@main_bp.route("/register", methods=["GET", "POST"])
def register_process():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))

    if request.method == "POST":
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        username = request.form.get("username")
        email = request.form.get("email")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        if password != confirm:
            return jsonify({
                'status': 'error',
                'message': 'Mật khẩu không khớp!',
                'status_code':400
            })

        extra_info = {
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "avatar": request.form.get("avatar"),
        }

        flag_created,msg = user_services.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_info
        )

        if flag_created:
            return {"status": "success", "message": "Đăng ký thành công!"}, 200
        else:
            return {"status": "error", "message": msg}, 400

    return render_template("register.html")

# ==========================================
# CART
# ==========================================
@main_bp.route('/cart')
@login_required
@role_required(UserRoleEnum.USER)
def cart_view():
    list_vouchers = voucher_services.load_vouchers(current_user.id)

    cart = session.get('cart', {})
    total_amount = sum(item['quantity'] * item['price'] for item in cart.values())
    total_quantity = sum(item['quantity'] for item in cart.values())

    return render_template('cart.html', list_vouchers=list_vouchers, total_amount=total_amount,total_quantity=total_quantity)

# Thêm API xử lý thêm vào giỏ hàng
@main_bp.route('/api/add-cart', methods=['POST'])
@login_required
@role_required(UserRoleEnum.USER)
def add_to_cart():
    data = request.json
    product_id = str(data.get('id'))
    name = data.get('name')
    price = float(data.get('price', 0))

    cart = session.get('cart')
    if not cart:
        cart = {}

    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'id': product_id,
            'name': name,
            'price': price,
            'quantity': 1
        }

    session['cart'] = cart

    total_quantity = sum(item['quantity'] for item in cart.values())
    total_amount = sum(item['quantity'] * item['price'] for item in cart.values())

    return jsonify({
        'status': 200,
        'total_quantity': total_quantity,
        'total_amount': total_amount,
        'message': 'Đã thêm thành công!'
    })


# API Cập nhật số lượng trong giỏ hàng
@main_bp.route('/api/update-cart', methods=['PUT'])
@login_required
@role_required(UserRoleEnum.USER)
def update_cart():
    data = request.json
    product_id = str(data.get('id'))
    quantity = int(data.get('quantity', 1))

    cart = session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] = quantity
        session['cart'] = cart
        session.modified = True

        item_total = cart[product_id]['price'] * quantity

        total_amount = sum(item['quantity'] * item['price'] for item in cart.values())
        total_quantity = sum(item['quantity'] for item in cart.values())

        return jsonify({
            'status': 200,
            'item_total': item_total,
            'total_amount': total_amount,
            'total_quantity': total_quantity
        })

    return jsonify({'status': 404, 'message': 'Không tìm thấy sản phẩm'})


# API Xóa sản phẩm khỏi giỏ hàng
@main_bp.route('/api/delete-cart', methods=['DELETE'])
@login_required
@role_required(UserRoleEnum.USER)
def delete_cart():
    data = request.json
    product_id = str(data.get('id'))

    cart = session.get('cart', {})

    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        session.modified = True

        total_amount = sum(item['quantity'] * item['price'] for item in cart.values())
        total_quantity = sum(item['quantity'] for item in cart.values())

        return jsonify({
            'status': 200,
            'total_amount': total_amount,
            'total_quantity': total_quantity
        })

    return jsonify({'status': 404, 'message': 'Không tìm thấy sản phẩm'})


# API Thanh toán đơn hàng
@main_bp.route('/api/pay', methods=['POST'])
@login_required
@role_required(UserRoleEnum.USER)
def pay():
    if not current_user.is_authenticated:
        return jsonify({'status': 401, 'message': 'Vui lòng đăng nhập để thanh toán!'})

    cart = session.get('cart', {})
    if not cart:
        return jsonify({'status': 400, 'message': 'Giỏ hàng của bạn đang trống!'})

    data = request.json
    voucher_code = data.get('voucher_code')
    success = order_services.create_order(current_user.id, cart, voucher_code)

    if success:
        session.pop('cart', None)
        session.modified = True
        return jsonify({'status': 200, 'message': 'Đặt hàng thành công!'})
    else:
        return jsonify({'status': 500, 'message': 'Có lỗi xảy ra khi tạo đơn hàng!'})

# ==========================================
# 5. LỊCH SỬ ĐƠN HÀNG
# ==========================================
@main_bp.route('/order_history')
@login_required
@role_required(UserRoleEnum.USER)
def order_history():
    list_orders = order_services.load_orders(current_user.id)
    return render_template('order_history.html',list_orders=list_orders)
