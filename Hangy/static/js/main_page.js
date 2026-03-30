document.addEventListener("DOMContentLoaded", function() {

    // ===========================================
    // 1. Chuyển màu header khi scroll
    // ===========================================
    const header = document.querySelector('.main-header');
    if (header) {
        // Hiệu ứng đổi màu khi cuộn
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        });
    }
});