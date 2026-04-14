// số có dấu phẩy phân cách hàng nghìn 1,000,000
let formatter = new Intl.NumberFormat('en-US');

document.addEventListener("DOMContentLoaded", function() {

    // đổi màu header khi scroll
    const header = document.querySelector('.main-header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }

});


function addToCart(id, name, price) {
    fetch('/api/add-cart', {
        method: 'POST',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        alert('Đã thêm "' + name + '" vào giỏ hàng!');
    });
}

function updateCart(id, obj) {
    let newQuantity = parseInt(obj.value);

    // số lượng sản phẩm bé hơn 0 thì xóa
    if (newQuantity <= 0 || isNaN(newQuantity)) {
        //Nếu khách hàng không xóa sản phẩm thì số lượng = 1
        obj.value = 1;
        deleteCart(id);
        return;
    }

    fetch('/api/update-cart', {
        method: 'PUT',
        body: JSON.stringify({
            "id": id,
            "quantity": newQuantity
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
        // cập nhật "Thành tiền" của  riêng 1 sản phẩm
        let itemTotal = document.getElementById(`item-total-${id}`);
        if (itemTotal) {
            itemTotal.innerText = formatter.format(data.item_total) + " ₫";
        }

        // cập nhật "Tổng tiền hàng" của đơn hàng
        let totalAmount = document.getElementById('total-amount');
        if (totalAmount) {
            totalAmount.innerText = formatter.format(data.total_amount) + " ₫";
            // gán thành tiền (số nguyên thủy) vào data-total để có thể thực hiện tính toán
            totalAmount.setAttribute('data-total', data.total_amount);
        }

        applyVoucher();
    });
}

function deleteCart(id) {
    // Hỏi người dùng cho chắc chắn
    if (confirm("Bạn có chắc chắn muốn xóa sản phẩm này khỏi giỏ hàng?")) {
        fetch('/api/delete-cart', {
            method: 'DELETE',
            body: JSON.stringify({
                "id": id
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            // 1. Xóa dòng (thẻ <tr>) chứa sản phẩm đó khỏi màn hình
            let product = document.getElementById(`cart${id}`);
            if (product) {
                product.remove();
            }

            // 2. Cập nhật "Tổng tiền hàng" và gán lại giá trị thô vào data-total
            let totalAmount = document.getElementById('total-amount');

            if (totalAmount) {
                totalAmount.innerText = formatter.format(data.total_amount) + " ₫";
                totalAmount.setAttribute('data-total', data.total_amount);
            }

            // 3. Gọi hàm tự động tính toán lại tiền Voucher và Tổng thanh toán
            applyVoucher();

            // 4. Nếu giỏ hàng đã trống trơn, tải lại trang
            if (data.total_quantity === 0) {
                location.reload();
            }
        });
    }
}

function applyVoucher() {
    let totalAmount = document.getElementById('total-amount');
    if (!totalAmount) return;

    // Lấy tổng tiền hàng dạng số (đã giấu trong thuộc tính data-total)
    let total = parseFloat(totalAmount.getAttribute('data-total')) || 0;

    // Lấy thẻ Select và Option đang được chọn
    let select = document.getElementById('voucher-select');
    let option = select.options[select.selectedIndex];

    // Lấy kiểu giảm (AMOUNT/PERCENT) và con số giảm giá
    let type = option.getAttribute('data-type');
    let value = parseFloat(option.getAttribute('data-value')) || 0;

    let discount = 0;

    // Tính tiền giảm giá
    if (type === 'PERCENT') {
        discount = total * (value / 100);
    } else if (type === 'AMOUNT') {
        discount = value;
    }

    // Đảm bảo không bao giờ giảm lố qua mức tổng tiền hàng (VD: đơn 50k không thể dùng mã giảm 100k thành âm tiền)
    if (discount > total) {
        discount = total;
    }

    // Tính tổng thanh toán cuối cùng
    let finalAmount = total - discount;

    // Hiển thị lên màn hình
    let discountElem = document.getElementById('voucher-discount');
    let finalElem = document.getElementById('final-amount');

    if (discountElem) discountElem.innerText = formatter.format(discount) + " ₫";
    if (finalElem) finalElem.innerText = formatter.format(finalAmount) + " ₫";
}

function pay() {
    // Lấy mã Voucher đang được chọn trên màn hình
    let select = document.getElementById('voucher-select');
    let voucherCode = select ? select.value : "";

    fetch('/api/pay', {
        method: 'POST',
        body: JSON.stringify({
            "voucher_code": voucherCode
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(res => res.json())
    .then(data => {
            alert(data.message);
            // Thành công -> Chuyển thẳng sang trang Lịch sử đơn hàng
            window.location.href = '/order_history';
    });
}