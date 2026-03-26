document.addEventListener("DOMContentLoaded", function () {
    const animatedItems = document.querySelectorAll(
        ".kpi-card, .status-box, .panel, .sidebar-nav a, .hero-btn, .quick-actions a, .mini-btn"
    );

    animatedItems.forEach((item, index) => {
        item.style.opacity = "0";
        item.style.transform = "translateY(14px)";

        setTimeout(() => {
            item.style.transition = "all 0.35s ease";
            item.style.opacity = "1";
            item.style.transform = "translateY(0)";
        }, index * 35);
    });

    const sidebarLinks = document.querySelectorAll(".sidebar-nav a");
    const currentPath = window.location.pathname;

    sidebarLinks.forEach((link) => {
        if (link.getAttribute("href") === currentPath) {
            sidebarLinks.forEach((item) => item.classList.remove("active"));
            link.classList.add("active");
        }
    });
});