#!/bin/bash

# ÉP PHIÊN LÀM VIỆC DÙNG UTF-8
export PYTHONIOENCODING=utf-8
export LANG=C.UTF-8

pip install -r requirements.txt

echo "=== 1. Cài đặt thư viện ==="
pip install Flask Flask-SQLAlchemy Flask-Login Faker pymysql

echo "=== 2. Reset Database và Chèn dữ liệu (Faker Seed) ==="
python <<EOF
import random
import hashlib
from faker import Faker
from datetime import datetime, timedelta

# Import đúng các Class từ cấu trúc model của bạn
try:
    from Hangy import db, app
    from Hangy.models import (
        User, Category, Product, Voucher, UserVoucher,
        UserRoleEnum, DiscountEnum, OrderStatus, Order, OrderDetail
    )
except ImportError as e:
    print(f"Lỗi Import: {e}")
    exit(1)

fake = Faker('vi_VN')
SEED_VALUE = 123
random.seed(SEED_VALUE)
fake.seed_instance(SEED_VALUE)

def hash_password(password):
    return hashlib.md5(password.strip().encode("utf-8")).hexdigest()

with app.app_context():
    print("-> Đang xóa sạch bảng cũ và tạo lại...")
    db.drop_all()
    db.create_all()

    # --- 1. Tạo Categories ---
    print("-> Đang tạo danh mục...")
    cat_names = ["Dụng cụ nhà bếp", "Bát đĩa", "Gia vị", "Đồ gỗ", "Inox"]
    categories = []
    for name in cat_names:
        c = Category(name=name)
        db.session.add(c)
        categories.append(c)
    db.session.commit()

    # --- 2. Tạo Users ---
    print("-> Đang tạo người dùng...")
    users = []
    pass_123 = hash_password("123")

    # Tạo 1 Admin mẫu
    admin_user = User(
        username="admin", password=pass_123, role=UserRoleEnum.ADMIN,
        first_name="Quản", last_name="Trị", email="admin@hangy.vn", address="Trụ sở chính Hangy"
    )
    db.session.add(admin_user)
    users.append(admin_user)

    for i in range(49):
        u = User(
            username=f"user_{i}", password=pass_123, role=UserRoleEnum.USER,
            first_name=fake.first_name(), last_name=fake.last_name(),
            email=f"user{i}@example.com", phone=fake.phone_number()[:15], address=fake.address()[:200]
        )
        users.append(u)
        db.session.add(u)
    db.session.commit()

    # --- 3. Tạo Vouchers ---
    print("-> Đang tạo mã giảm giá...")
    vouchers = []
    for i in range(20):
        v_type = DiscountEnum.PERCENT if i % 2 == 0 else DiscountEnum.AMOUNT
        # Tuân thủ Validator: PERCENT không quá 50%
        v_val = float(random.randint(5, 30)) if v_type == DiscountEnum.PERCENT else float(random.randint(20, 100)*1000)

        v = Voucher(
            code=f"HANGY_{i:02d}", discount_type=v_type, discount_value=v_val,
            end_date=datetime.now() + timedelta(days=random.randint(30, 365))
        )
        db.session.add(v)
        vouchers.append(v)
    db.session.commit()

    # --- 4. Tạo Sản phẩm ---
    print("-> Đang tạo sản phẩm...")
    items = ["Bát sứ", "Thìa gỗ", "Hũ gia vị", "Muôi inox", "Chảo gang"]
    products_list = []
    for i in range(100):
        pr = Product(
            name=f"{items[i%5]} cao cấp số {i}",
            price=float(random.randint(10, 200)*5000),
            category_id=random.choice(categories).id
        )
        db.session.add(pr)
        products_list.append(pr)
    db.session.commit()

    # --- 5. Gán Voucher cho người dùng ---
    print("-> Đang phát voucher cho người dùng...")
    regular_users = [u for u in users if u.role == UserRoleEnum.USER]
    for u in regular_users:
        selected_vouchers = random.sample(vouchers, k=random.randint(1, 3))
        for v in selected_vouchers:
            uv = UserVoucher(user_id=u.id, voucher_id=v.id, is_used=False)
            db.session.add(uv)
    db.session.commit()

    # --- 6. Tạo Đơn hàng mẫu (MỚI) ---
    print("-> Đang tạo đơn hàng và chi tiết đơn hàng mẫu...")
    for i in range(20):
        u = random.choice(regular_users)
        # Lấy 1 voucher chưa dùng của user này (nếu có)
        uv = UserVoucher.query.filter_by(user_id=u.id, is_used=False).first()

        order = Order(
            user_id=u.id, total_amount=0, final_amount=0,
            status=random.choice(list(OrderStatus))
        )
        db.session.add(order)
        db.session.flush() # Lấy ID đơn hàng trước khi commit

        total = 0
        # Chọn ngẫu nhiên 1-4 sản phẩm cho đơn hàng
        for pr in random.sample(products_list, k=random.randint(1, 4)):
            qty = random.randint(1, 3)
            detail = OrderDetail(
                order_id=order.id, product_id=pr.id,
                quantity=qty, price=pr.price # Lưu giá tại thời điểm mua
            )
            total += pr.price * qty
            db.session.add(detail)

        order.total_amount = total
        discount = 0
        if uv and random.choice([True, False]): # Ngẫu nhiên quyết định có dùng voucher không
            v = uv.voucher
            discount = (total * (v.discount_value / 100)) if v.discount_type == DiscountEnum.PERCENT else v.discount_value
            uv.is_used = True
            uv.order_id = order.id
            uv.used_date = datetime.now()

        order.final_amount = max(0, total - discount)

    db.session.commit()
    print("-> THÀNH CÔNG: Database đã sẵn sàng với đầy đủ dữ liệu mẫu.")
EOF

echo "=== 3. Khởi động Flask Server ==="
export FLASK_APP=Hangy
export FLASK_DEBUG=1
flask run