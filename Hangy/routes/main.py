import math

from flask import render_template, request, redirect, url_for, flash, Blueprint
from sqlalchemy.sql.functions import current_user
from flask_login import login_user, logout_user, current_user


from Hangy import PAGE_SIZE, login
from Hangy.services import user_service, products

main_bp = Blueprint("main_bp", __name__, template_folder="../templates/Main_Page")


@main_bp.route("/")
def index():
    kw = request.args.get("kw")

    page = request.args.get("page", 1, type=int)

    page_size = PAGE_SIZE

    list_products, total = products.load_products(kw=kw, page=page, page_size=page_size)
    total_pages = math.ceil(total / page_size)

    return render_template(
        "index.html",
        list_products=list_products,
        total_pages=total_pages,
        current_user=current_user,
    )


# ==========================================
# LOGIN / LOGOUT / LOAD USER
# ==========================================
@login.user_loader
def load_user(user_id):
    return user_service.get_user_by_id(int(user_id))


@main_bp.route("/login", methods=["GET", "POST"])
def login_process():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = user_service.authenticate(username=username, password=password)

        if user:
            login_user(user)
            return redirect(request.args.get("next") or url_for("main_bp.index"))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng!", "danger")
            return render_template("login.html")

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
            flash("Mật khẩu không khớp!", "danger")
            return render_template("register.html")

        extra_info = {
            "phone": request.form.get("phone"),
            "address": request.form.get("address"),
            "avatar": request.form.get("avatar"),
        }

        if user_service.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_info
        ):
            flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
            return redirect(url_for("main_bp.login_process"))
        else:
            flash("Đăng ký thất bại! Tài khoản hoặc Email đã tồn tại.", "danger")

    return render_template("register.html")
