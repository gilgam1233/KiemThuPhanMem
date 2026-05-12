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
    let cartLocal = localStorage.getItem('cart-quantity')
    let cartNumber = document.getElementById('total-quantity')

    if (cartNumber && cartLocal && parseInt(cartLocal) > 0) {
        cartNumber.innerText = cartLocal;
    }

    const uploadBtn = document.getElementById("upload_widget");
    if (uploadBtn)
    {
        var myWidget = cloudinary.createUploadWidget({
            cloudName: 'dvvvepfpu',
            uploadPreset: 'hangy_cloudinary',
            sources: ['local', 'url', 'camera'],
            multiple: false,
            cropping: true,
            croppingAspectRatio: 1,
            showSkipCropButton: false,
            folder: 'hangy'
        }, (error, result) => {
            if (!error && result && result.event === "success") {
                var imageUrl = result.info.secure_url;
                const previewImg = document.getElementById("avatarPreview");
                if (previewImg) previewImg.src = imageUrl;

                const avatarInput = document.getElementById("avatarInput");
                if (avatarInput) avatarInput.value = imageUrl;

                const newAvatarInput = document.getElementById("newAvatarInput");
                if (newAvatarInput) newAvatarInput.value = imageUrl;

                const updateForm = document.getElementById("avatarUpdateForm");
                if (updateForm) updateForm.submit();
            }
        });
        uploadBtn.addEventListener("click", function(){ myWidget.open(); }, false);
    }
});

function loginProcess() {
    fetch('/login', {
        method: 'POST',
        body: new FormData(document.getElementById('loginForm'))
    }).then(res => res.json()).then(data => {
        if (data.status==='success') {
            window.location.href=data.next;
        }
        else {
            Swal.fire({
                title: "Đăng nhập thất bại",
                text: data.message,
                icon: "error"
            })

        }
    }).catch(err => {
        Swal.fire('Lỗi', 'Không thể kết nối đến máy chủ. Vui lòng thử lại sau!', 'error');
    })
}

function registerProcess() {
    fetch('/register', {
        method: 'POST',
        body: new FormData(document.getElementById('registerForm'))
    }).then(res => res.json()).then(data => {
        if (data.status==='success') {
            Swal.fire({
                title: "Đăng ký thành công",
                icon: "success",
                showConfirmButton: false,
                timer: 1000
            }).then(() => window.location.href='/login')
        }
        else {
            Swal.fire({
                title: "Đăng ký thất bại",
                text: data.message,
                icon: "error"
            })
        }
    }).catch(err => {
        Swal.fire('Lỗi', 'Không thể kết nối đến máy chủ. Vui lòng thử lại sau!', 'error');
    })
}


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
    .then(res => res.json()).then(data => {
        Swal.fire({
            title: data.message,
            icon: "success",
            showConfirmButton: false,
            timer: 1000
        });

        localStorage.setItem('cart-quantity',data.total_quantity);
        document.getElementById('total-quantity').innerText = data.total_quantity;

    });
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
        // cập nhật cart number
        let cartNumber = document.getElementById('total-quantity');
        if (cartNumber) {
            cartNumber.innerText = data.total_quantity
        }

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
        localStorage.setItem('cart-quantity',data.total_quantity);
        document.getElementById('total-quantity').innerText = data.total_quantity;
    });
}

function deleteCart(id) {
    Swal.fire({
        title: "Chắc chắn xoá?",
        text: "Bạn có chắc chắn muốn xoá sản phẩm khỏi giỏ hàng? Không thể hoàn tác thao tác!",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "Xác nhận",
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire({
                title: "Thành công!",
                text: "Đã xoá sản phẩm khỏi giỏ hàng.",
                icon: "success",
                showConfirmButton: false,
                timer: 1000
            });
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

            // cập nhật cart number
            let cartNumber = document.getElementById('total-quantity');
            if (cartNumber) {
                cartNumber.innerText = data.total_quantity
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

            localStorage.setItem('cart-quantity',data.total_quantity);
            document.getElementById('total-quantity').innerText = data.total_quantity;
        });
        }
});
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
        if (data.status === 200) {
            Swal.fire({
                title: "Thành công!",
                text: data.message,
                icon: "success",
                showConfirmButton: false,
                timer: 1000
            })
        }
        else {
            Swal.fire({
                title: "Thất bại!",
                text: data.message,
                icon: "error"
            })
        }
        localStorage.removeItem('cart-quantity');
        document.getElementById('total-quantity').innerText='';
        window.location.href = '/order_history';
    });
}

