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
    .then(res => res.json());
}

function updateCart(id, obj) {
    let newQuantity = parseInt(obj.value);

    // số lượng sản phẩm bé hơn 0 thì xóa
    if (newQuantity <= 0 || isNaN(newQuantity)) {
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
            let product = document.getElementById(`cart${id}`);
            if (product) {
                product.remove();
            }

            // cập nhật "Tổng tiền hàng" của đơn hàng
            let totalAmount = document.getElementById('total-amount');

            if (totalAmount) {
                totalAmount.innerText = formatter.format(data.total_amount) + " ₫";
                totalAmount.setAttribute('data-total', data.total_amount);
            }

            applyVoucher();

            if (data.total_quantity === 0) {
                location.reload();
            }
        });
    }
}

function applyVoucher() {
    let totalAmount = document.getElementById('total-amount');
    if (!totalAmount) return;

    let total = parseFloat(totalAmount.getAttribute('data-total')) || 0;

    let select = document.getElementById('voucher-select');
    let option = select.options[select.selectedIndex];

    let type = option.getAttribute('data-type');
    let value = parseFloat(option.getAttribute('data-value')) || 0;

    let discount = 0;

    if (type === 'PERCENT') {
        discount = total * (value / 100);
    } else if (type === 'AMOUNT') {
        discount = value;
    }

    if (discount > total) {
        discount = total;
    }

    let finalAmount = total - discount;

    let discountElem = document.getElementById('voucher-discount');
    let finalElem = document.getElementById('final-amount');

    if (discountElem) discountElem.innerText = formatter.format(discount) + " ₫";
    if (finalElem) finalElem.innerText = formatter.format(finalAmount) + " ₫";
}

function pay() {
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
            window.location.href = '/order_history';
    });
}